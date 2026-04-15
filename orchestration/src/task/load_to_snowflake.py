import os

import snowflake.connector
from dotenv import load_dotenv
from prefect import get_run_logger

load_dotenv()

TRUNCATE_STAGING = "TRUNCATE TABLE RAW_DPWH_PROJECTS_STAGING"

COPY_INTO_STAGING = """
    COPY INTO RAW_DPWH_PROJECTS_STAGING (
        CONTRACTID, DESCRIPTION, CATEGORY, COMPONENTCATEGORIES,
        STATUS, BUDGET, AMOUNTPAID, PROGRESS, CONTRACTOR,
        STARTDATE, COMPLETIONDATE, INFRAYEAR, PROGRAMNAME,
        SOURCEOFFUNDS, ISLIVE, LIVESTREAMURL, LIVESTREAMVIDEOID,
        LIVESTREAMDETECTEDAT, LATITUDE, LONGITUDE, REPORTCOUNT,
        HASSATELLITEIMAGE, PROVINCE, REGION
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
    FORCE = TRUE
"""

MERGE_INTO_RAW = """
    MERGE INTO RAW_DPWH_PROJECTS t
    USING RAW_DPWH_PROJECTS_STAGING s
        ON t.CONTRACTID = s.CONTRACTID
    WHEN MATCHED AND (
        t.STATUS != s.STATUS OR
        t.PROGRESS != s.PROGRESS OR
        t.AMOUNTPAID != s.AMOUNTPAID OR
        t.CONTRACTOR != s.CONTRACTOR OR
        t.DESCRIPTION != s.DESCRIPTION OR
        t.CATEGORY != s.CATEGORY OR
        t.COMPONENTCATEGORIES != s.COMPONENTCATEGORIES OR
        t.BUDGET != s.BUDGET OR
        t.STARTDATE != s.STARTDATE OR
        t.INFRAYEAR != s.INFRAYEAR OR
        t.PROGRAMNAME != s.PROGRAMNAME OR
        t.SOURCEOFFUNDS != s.SOURCEOFFUNDS OR
        t.ISLIVE != s.ISLIVE OR
        NOT EQUAL_NULL(t.COMPLETIONDATE, s.COMPLETIONDATE) OR
        NOT EQUAL_NULL(t.LIVESTREAMURL, s.LIVESTREAMURL) OR
        NOT EQUAL_NULL(t.LIVESTREAMVIDEOID, s.LIVESTREAMVIDEOID) OR
        NOT EQUAL_NULL(t.LIVESTREAMDETECTEDAT, s.LIVESTREAMDETECTEDAT) OR
        t.LATITUDE != s.LATITUDE OR
        t.LONGITUDE != s.LONGITUDE OR
        t.REPORTCOUNT != s.REPORTCOUNT OR
        t.HASSATELLITEIMAGE != s.HASSATELLITEIMAGE OR
        t.PROVINCE != s.PROVINCE OR
        t.REGION != s.REGION
    ) THEN UPDATE SET
        t.STATUS               = s.STATUS,
        t.PROGRESS             = s.PROGRESS,
        t.AMOUNTPAID           = s.AMOUNTPAID,
        t.COMPLETIONDATE       = s.COMPLETIONDATE,
        t.CONTRACTOR           = s.CONTRACTOR,
        t.DESCRIPTION          = s.DESCRIPTION,
        t.CATEGORY             = s.CATEGORY,
        t.COMPONENTCATEGORIES  = s.COMPONENTCATEGORIES,
        t.BUDGET               = s.BUDGET,
        t.STARTDATE            = s.STARTDATE,
        t.INFRAYEAR            = s.INFRAYEAR,
        t.PROGRAMNAME          = s.PROGRAMNAME,
        t.SOURCEOFFUNDS        = s.SOURCEOFFUNDS,
        t.ISLIVE               = s.ISLIVE,
        t.LIVESTREAMURL        = s.LIVESTREAMURL,
        t.LIVESTREAMVIDEOID    = s.LIVESTREAMVIDEOID,
        t.LIVESTREAMDETECTEDAT = s.LIVESTREAMDETECTEDAT,
        t.LATITUDE             = s.LATITUDE,
        t.LONGITUDE            = s.LONGITUDE,
        t.REPORTCOUNT          = s.REPORTCOUNT,
        t.HASSATELLITEIMAGE    = s.HASSATELLITEIMAGE,
        t.PROVINCE             = s.PROVINCE,
        t.REGION               = s.REGION,
        t.LAST_UPDATED_AT      = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN INSERT (
        CONTRACTID, DESCRIPTION, CATEGORY, COMPONENTCATEGORIES,
        STATUS, BUDGET, AMOUNTPAID, PROGRESS, CONTRACTOR,
        STARTDATE, COMPLETIONDATE, INFRAYEAR, PROGRAMNAME,
        SOURCEOFFUNDS, ISLIVE, LIVESTREAMURL, LIVESTREAMVIDEOID,
        LIVESTREAMDETECTEDAT, LATITUDE, LONGITUDE, REPORTCOUNT,
        HASSATELLITEIMAGE, PROVINCE, REGION, LAST_UPDATED_AT
    ) VALUES (
        s.CONTRACTID, s.DESCRIPTION, s.CATEGORY, s.COMPONENTCATEGORIES,
        s.STATUS, s.BUDGET, s.AMOUNTPAID, s.PROGRESS, s.CONTRACTOR,
        s.STARTDATE, s.COMPLETIONDATE, s.INFRAYEAR, s.PROGRAMNAME,
        s.SOURCEOFFUNDS, s.ISLIVE, s.LIVESTREAMURL, s.LIVESTREAMVIDEOID,
        s.LIVESTREAMDETECTEDAT, s.LATITUDE, s.LONGITUDE, s.REPORTCOUNT,
        s.HASSATELLITEIMAGE, s.PROVINCE, s.REGION, CURRENT_TIMESTAMP()
    )
"""


def load_to_snowflake() -> None:
    logger = get_run_logger()
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="RAW",
        role=os.getenv("SNOWFLAKE_ROLE"),
    )
    cur = conn.cursor()

    logger.info("Truncating staging table...")
    cur.execute(TRUNCATE_STAGING)

    logger.info("Loading parquet from S3 into staging...")
    cur.execute(COPY_INTO_STAGING)

    logger.info("Merging staging into raw table...")
    cur.execute(MERGE_INTO_RAW)

    cur.close()
    conn.close()
    logger.info("Snowflake load complete")
