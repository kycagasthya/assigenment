USE ROLE ETL_ROLE;
USE DATABASE ABS_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/ABS_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/ABS_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE_TO_LOWER function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_TO_LOWER(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE_TO_LOWER(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_TO_LOWER(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/ABS_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/ABS_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE ALPHA_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/ALPHA_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/ALPHA_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;



// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/ALPHA_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/ALPHA_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE BLUEBERRY_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/BLUEBERRY_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/BLUEBERRY_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/BLUEBERRY_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/BLUEBERRY_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE COMMON_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/COMMON_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/COMMON_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE EIGHTYONE_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/EIGHTYONE_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/EIGHTYONE_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/EIGHTYONE_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/EIGHTYONE_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE LOBSTER_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/LOBSTER_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/LOBSTER_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/LOBSTER_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/LOBSTER_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE MAF_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/MAF_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/MAF_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/MAF_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/MAF_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE SUNBIRD_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/SUNBIRD_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/SUNBIRD_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/SUNBIRD_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/SUNBIRD_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE TANGERINE_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/TANGERINE_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/TANGERINE_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE WINGS_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/WINGS_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINGS_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/WINGS_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINGS_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------

USE ROLE ETL_ROLE;
USE DATABASE WINTER_DEV;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/WINTER_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE json_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINTER_DEV/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export for datalake staging environment';

GRANT USAGE ON STAGE json_unload_file_stage_target_stg TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-dev-dl-sub-bq-9220-historical/WINTER_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

CREATE OR REPLACE STAGE csv_unload_file_stage_target_stg
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINTER_DEV/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage_target_stg TO ROLE ETL_ROLE;

------------------------------------------------------------------------------------------------------------------------


USE ROLE ETL_ROLE;
USE DATABASE WINGS_UAT;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINGS_UAT/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINGS_UAT/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;
USE ROLE ETL_ROLE;
USE DATABASE WINTER_UAT;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINTER_UAT/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-n-stg-dl-sub-bq-b703-historical/WINTER_UAT/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

------------------------------------------------------------
------------



USE ROLE ETL_ROLE;
USE DATABASE ABS;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/ABS/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/ABS/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE ALPHA;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/ALPHA/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/ALPHA/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE BLUEBERRY;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/BLUEBERRY/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/BLUEBERRY/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE COMMON;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/COMMON/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/COMMON/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE EIGHTYONE;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/EIGHTYONE/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/EIGHTYONE/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE LOBSTER;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/LOBSTER/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/LOBSTER/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE MAF;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/MAF/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/MAF/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE SUNBIRD;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/SUNBIRD/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/SUNBIRD/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE TANGERINE;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/TANGERINE/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;


// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/TANGERINE/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE WINGS;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/WINGS/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/WINGS/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

USE ROLE ETL_ROLE;
USE DATABASE WINTER;
USE SCHEMA DATA_LAKE;

-- file format will be created in wings_dev database and in data_lake schema
CREATE OR REPLACE FILE FORMAT json_unload_file_format
TYPE = JSON
SNAPPY_COMPRESSION = TRUE
COMMENT = 'FILE FORMAT FOR UNLOADING AS JSON NEWLINE DELIMITED FILES';

GRANT USAGE ON FILE FORMAT json_unload_file_format TO ROLE ETL_ROLE;

-- once used, this stage will place data to the path provided y URL
CREATE OR REPLACE STAGE json_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/WINTER/'
storage_integration = gcs_historical
FILE_FORMAT = json_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external JSON export';

GRANT USAGE ON STAGE json_unload_file_stage TO ROLE ETL_ROLE;

-- create KEYS_TO_SNAKE function
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey.replace(/-|\./g, "_");
changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE(element);
});
}

return O;
$$;

-- create KEYS_TO_SNAKE function with full conversion to snake case
CREATE OR REPLACE FUNCTION KEYS_TO_SNAKE_FULL(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
const changeCaseOfKey = key => {
  return key
    .replace(/\W+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map(word => word.toLowerCase())
    .join("_");
};

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = changeCaseOfKey(originalKey);
changedObject[newKey] = KEYS_TO_SNAKE_FULL(O[originalKey]);
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return KEYS_TO_SNAKE_FULL(element);
});
}

return O;
$$;

CREATE OR REPLACE FUNCTION REMOVE_NULLS(O VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
const changedObject = {};
Object.keys(O).forEach(originalKey => {
const newKey = originalKey;

if (O[originalKey] !== null) {
changedObject[newKey] = REMOVE_NULLS(O[originalKey]);
}
});
return changedObject;
} else if (Array.isArray(O)) {
return O.map(element => {
return REMOVE_NULLS(element);
});
}

return O;
$$;

-- create ADD_MISSING_EMBEDDED_COLUMNS function
CREATE OR REPLACE FUNCTION ADD_MISSING_EMBEDDED_COLUMNS(O VARIANT, PARENTFIELDNAME STRING, MISSINGFIELDNAME STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$

if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
  if (Object.keys(O).includes('pick')) {
      O['pick']['barcodes'].forEach(singleBarcode => {
        if (!(Object.keys(singleBarcode).includes(MISSINGFIELDNAME))) {
          singleBarcode[MISSINGFIELDNAME] = -100
        }
        if (Object.keys(singleBarcode).includes('variableMeasure')) {
          if (!(Object.keys(singleBarcode['variableMeasure']).includes('middleCheckDigit'))) {
            singleBarcode['variableMeasure']['middleCheckDigit'] = -100
          }
        }
      })
  }
  return O
} else if (Array.isArray(O)) {
  return O.map(element => {
  return ADD_MISSING_EMBEDDED_COLUMNS(element);
});
}

return O;
$$;

// file format
CREATE OR REPLACE FILE FORMAT csv_unload_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
COMPRESSION = GZIP
COMMENT = 'FILE FORMAT FOR UNLOADING AS CSV FILES';

GRANT USAGE ON FILE FORMAT csv_unload_file_format TO ROLE ETL_ROLE;

// file stage
CREATE OR REPLACE STAGE csv_unload_file_stage
URL = 'gcs://prj-daas-p-prd-dl-sub-bq-historical/WINTER/csv'
storage_integration = gcs_historical
FILE_FORMAT = csv_unload_file_format
COMMENT = 'GCS Stage for the Snowflake external CSV export';

GRANT USAGE ON STAGE csv_unload_file_stage TO ROLE ETL_ROLE;

