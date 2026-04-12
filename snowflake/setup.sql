-- ============================================================
-- DPWH PROJECTS PIPELINE — SNOWFLAKE SETUP
-- Run these in order
-- ============================================================


-- ------------------------------------------------------------
-- STEP 1: DATABASE AND SCHEMA
-- ------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS DPWH_PROJECTS_DB;

CREATE SCHEMA IF NOT EXISTS DPWH_PROJECTS_DB.RAW;
CREATE SCHEMA IF NOT EXISTS DPWH_PROJECTS_DB.DEV;
CREATE SCHEMA IF NOT EXISTS DPWH_PROJECTS_DB.PROD;

GRANT ALL PRIVILEGES ON DATABASE DPWH_PROJECTS_DB TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON SCHEMA DPWH_PROJECTS_DB.RAW TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON SCHEMA DPWH_PROJECTS_DB.DEV TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON SCHEMA DPWH_PROJECTS_DB.PROD TO ROLE DATA_ENGINEER;


GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA DPWH_PROJECTS_DB.RAW TO ROLE DATA_ENGINEER;
GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA DPWH_PROJECTS_DB.DEV TO ROLE DATA_ENGINEER;
GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA DPWH_PROJECTS_DB.PROD TO ROLE DATA_ENGINEER;


-- ------------------------------------------------------------
-- STEP 2: STAGE
-- Points to the single parquet file in S3
-- This file gets overwritten every monthly run
-- ------------------------------------------------------------

CREATE OR REPLACE STAGE DPWH_PROJECTS_DB.RAW.DPWH_PROJECTS_STAGE
    URL = 's3://dpwh-projects-s3-bucket-126961545681-ap-southeast-1-an/raw/'
    CREDENTIALS = (
        AWS_KEY_ID = 'YOUR_AWS_KEY_ID'
        AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
    )
    FILE_FORMAT = (
        TYPE = 'PARQUET'
        SNAPPY_COMPRESSION = TRUE
    );

GRANT USAGE ON STAGE DPWH_PROJECTS_DB.RAW.DPWH_PROJECTS_STAGE TO ROLE DATA_ENGINEER;
GRANT READ ON STAGE DPWH_PROJECTS_DB.RAW.DPWH_PROJECTS_STAGE TO ROLE DATA_ENGINEER;

-- verify stage is working
LIST @DPWH_PROJECTS_DB.RAW.DPWH_PROJECTS_STAGE;


-- ------------------------------------------------------------
-- STEP 3: STAGING TABLE (middleman — truncated every run)
-- Holds the full fresh extract before merging into raw
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS_STAGING (
    CONTRACTID            VARCHAR,
    DESCRIPTION           VARCHAR,
    CATEGORY              VARCHAR,
    COMPONENTCATEGORIES   VARCHAR,
    STATUS                VARCHAR,
    BUDGET                DOUBLE,
    AMOUNTPAID            NUMBER,
    PROGRESS              DOUBLE,
    CONTRACTOR            VARCHAR,
    STARTDATE             VARCHAR,
    COMPLETIONDATE        VARCHAR,
    INFRAYEAR             VARCHAR,
    PROGRAMNAME           VARCHAR,
    SOURCEOFFUNDS         VARCHAR,
    ISLIVE                BOOLEAN,
    LIVESTREAMURL         VARCHAR,
    LIVESTREAMVIDEOID     VARCHAR,
    LIVESTREAMDETECTEDAT  VARCHAR,
    LATITUDE              DOUBLE,
    LONGITUDE             DOUBLE,
    REPORTCOUNT           NUMBER,
    HASSATELLITEIMAGE     BOOLEAN,
    PROVINCE              VARCHAR,
    REGION                VARCHAR
);


-- ------------------------------------------------------------
-- STEP 4: RAW TABLE (permanent — only touched via MERGE)
-- Accumulates all records over time
-- Includes last_updated_at to track when a row last changed
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS (
    CONTRACTID            VARCHAR        NOT NULL,
    DESCRIPTION           VARCHAR,
    CATEGORY              VARCHAR,
    COMPONENTCATEGORIES   VARCHAR,
    STATUS                VARCHAR,
    BUDGET                DOUBLE,
    AMOUNTPAID            NUMBER,
    PROGRESS              DOUBLE,
    CONTRACTOR            VARCHAR,
    STARTDATE             VARCHAR,
    COMPLETIONDATE        VARCHAR,
    INFRAYEAR             VARCHAR,
    PROGRAMNAME           VARCHAR,
    SOURCEOFFUNDS         VARCHAR,
    ISLIVE                BOOLEAN,
    LIVESTREAMURL         VARCHAR,
    LIVESTREAMVIDEOID     VARCHAR,
    LIVESTREAMDETECTEDAT  VARCHAR,
    LATITUDE              DOUBLE,
    LONGITUDE             DOUBLE,
    REPORTCOUNT           NUMBER,
    HASSATELLITEIMAGE     BOOLEAN,
    PROVINCE              VARCHAR,
    REGION                VARCHAR,
    LAST_UPDATED_AT       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT PK_DPWH_PROJECTS PRIMARY KEY (CONTRACTID)
);


-- ============================================================
-- MONTHLY PIPELINE — Run these every month in order
-- ============================================================


-- ------------------------------------------------------------
-- STEP 5: TRUNCATE STAGING
-- Wipe the middleman table clean before loading fresh data
-- ------------------------------------------------------------

TRUNCATE TABLE DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS_STAGING;


-- ------------------------------------------------------------
-- STEP 6: COPY FROM S3 INTO STAGING
-- FORCE = TRUE ensures Snowflake reloads the file
-- even if it has seen this filename before
-- ------------------------------------------------------------

COPY INTO DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS_STAGING (
    CONTRACTID,
    DESCRIPTION,
    CATEGORY,
    COMPONENTCATEGORIES,
    STATUS,
    BUDGET,
    AMOUNTPAID,
    PROGRESS,
    CONTRACTOR,
    STARTDATE,
    COMPLETIONDATE,
    INFRAYEAR,
    PROGRAMNAME,
    SOURCEOFFUNDS,
    ISLIVE,
    LIVESTREAMURL,
    LIVESTREAMVIDEOID,
    LIVESTREAMDETECTEDAT,
    LATITUDE,
    LONGITUDE,
    REPORTCOUNT,
    HASSATELLITEIMAGE,
    PROVINCE,
    REGION
)
FROM (
    SELECT
        $1:contractId::VARCHAR,
        $1:description::VARCHAR,
        $1:category::VARCHAR,
        $1:componentCategories::VARCHAR,
        $1:status::VARCHAR,
        $1:budget::DOUBLE,
        $1:amountPaid::NUMBER,
        $1:progress::DOUBLE,
        $1:contractor::VARCHAR,
        $1:startDate::VARCHAR,
        $1:completionDate::VARCHAR,
        $1:infraYear::VARCHAR,
        $1:programName::VARCHAR,
        $1:sourceOfFunds::VARCHAR,
        $1:isLive::BOOLEAN,
        $1:livestreamUrl::VARCHAR,
        $1:livestreamVideoId::VARCHAR,
        $1:livestreamDetectedAt::VARCHAR,
        $1:latitude::DOUBLE,
        $1:longitude::DOUBLE,
        $1:reportCount::NUMBER,
        $1:hasSatelliteImage::BOOLEAN,
        $1:province::VARCHAR,
        $1:region::VARCHAR
    FROM @DPWH_PROJECTS_DB.RAW.DPWH_PROJECTS_STAGE/dpwh_projects_raw.parquet
)
FILE_FORMAT = (TYPE = 'PARQUET')
FORCE = TRUE;

-- verify staging loaded correctly
SELECT COUNT(*) FROM DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS_STAGING;


-- ------------------------------------------------------------
-- STEP 7: MERGE STAGING INTO RAW TABLE
-- INSERT new contractIds
-- UPDATE rows where status or progress changed
-- SKIP rows where nothing changed
-- ------------------------------------------------------------

MERGE INTO DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS t
USING DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS_STAGING s
    ON t.CONTRACTID = s.CONTRACTID

WHEN MATCHED AND (
    t.STATUS != s.STATUS OR
    t.PROGRESS != s.PROGRESS OR
    t.AMOUNTPAID != s.AMOUNTPAID OR
    t.COMPLETIONDATE != s.COMPLETIONDATE
) THEN UPDATE SET
    t.STATUS               = s.STATUS,
    t.PROGRESS             = s.PROGRESS,
    t.AMOUNTPAID           = s.AMOUNTPAID,
    t.COMPLETIONDATE       = s.COMPLETIONDATE,
    t.ISLIVE               = s.ISLIVE,
    t.LIVESTREAMURL        = s.LIVESTREAMURL,
    t.LIVESTREAMVIDEOID    = s.LIVESTREAMVIDEOID,
    t.LIVESTREAMDETECTEDAT = s.LIVESTREAMDETECTEDAT,
    t.REPORTCOUNT          = s.REPORTCOUNT,
    t.HASSATELLITEIMAGE    = s.HASSATELLITEIMAGE,
    t.LAST_UPDATED_AT      = CURRENT_TIMESTAMP()

WHEN NOT MATCHED THEN INSERT (
    CONTRACTID, DESCRIPTION, CATEGORY, COMPONENTCATEGORIES,
    STATUS, BUDGET, AMOUNTPAID, PROGRESS, CONTRACTOR,
    STARTDATE, COMPLETIONDATE, INFRAYEAR, PROGRAMNAME,
    SOURCEOFFUNDS, ISLIVE, LIVESTREAMURL, LIVESTREAMVIDEOID,
    LIVESTREAMDETECTEDAT, LATITUDE, LONGITUDE, REPORTCOUNT,
    HASSATELLITEIMAGE, PROVINCE, REGION, LAST_UPDATED_AT
)
VALUES (
    s.CONTRACTID, s.DESCRIPTION, s.CATEGORY, s.COMPONENTCATEGORIES,
    s.STATUS, s.BUDGET, s.AMOUNTPAID, s.PROGRESS, s.CONTRACTOR,
    s.STARTDATE, s.COMPLETIONDATE, s.INFRAYEAR, s.PROGRAMNAME,
    s.SOURCEOFFUNDS, s.ISLIVE, s.LIVESTREAMURL, s.LIVESTREAMVIDEOID,
    s.LIVESTREAMDETECTEDAT, s.LATITUDE, s.LONGITUDE, s.REPORTCOUNT,
    s.HASSATELLITEIMAGE, s.PROVINCE, s.REGION, CURRENT_TIMESTAMP()
);

-- verify raw table
SELECT COUNT(*) FROM DPWH_PROJECTS_DB.RAW.RAW_DPWH_PROJECTS;