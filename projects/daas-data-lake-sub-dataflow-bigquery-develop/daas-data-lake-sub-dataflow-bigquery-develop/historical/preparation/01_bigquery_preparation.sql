CREATE OR REPLACE FUNCTION dl_service.keys_to_snake(json_row STRING)
  RETURNS STRING
  LANGUAGE js AS r"""
function KEYS_TO_SNAKE(O) {
  if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
    const changedObject = {};
    Object.keys(O).forEach(originalKey => {
      const newKey = originalKey.replace(/-/g, "_");
      changedObject[newKey] = KEYS_TO_SNAKE(O[originalKey]);
    });
    return changedObject;
  } else if (Array.isArray(O)) {
    return O.map(element => {
      return KEYS_TO_SNAKE(element);
    });
  }

  return O;
}
var row = KEYS_TO_SNAKE(JSON.parse(json_row));
return JSON.stringify(row);
""";

CREATE OR REPLACE FUNCTION dl_service.keys_to_snake_to_lower(json_row STRING)
  RETURNS STRING
  LANGUAGE js AS r"""
function KEYS_TO_SNAKE_TO_LOWER(O) {
  if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
    const changedObject = {};
    Object.keys(O).forEach(originalKey => {
      const newKey = originalKey.replace(/-/g, "_");
      changedObject[newKey] = KEYS_TO_SNAKE_TO_LOWER(O[originalKey]);
    });
    return changedObject;
  } else if (Array.isArray(O)) {
    return O.map(element => {
      return KEYS_TO_SNAKE_TO_LOWER(element);
    });
  }

  return O;
}
var row = KEYS_TO_SNAKE_TO_LOWER(JSON.parse(json_row));
return JSON.stringify(row);
""";

CREATE OR REPLACE FUNCTION dl_service.remove_nulls(json_row STRING)
  RETURNS STRING
  LANGUAGE js AS r"""
function REMOVE_NULLS(O) {
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
    if (O.length !== 0) {
      return O.map(element => {
        return REMOVE_NULLS(element);
      });
    }
    else {
      return;
    }
  }

  return O;
}
var row = REMOVE_NULLS(JSON.parse(json_row));
return JSON.stringify(row);
""";

CREATE OR REPLACE FUNCTION dl_service.sort_json(json_row STRING)
  RETURNS STRING
  LANGUAGE js AS r"""
function SORT_JSON(O) {
  if (O === Object(O) && !Array.isArray(O) && typeof O !== "function") {
    const changedObject = {};
    Object.keys(O).sort().forEach(key => {
      changedObject[key] = SORT_JSON(O[key]);
    });
    return changedObject;
  } else if (Array.isArray(O)) {
    return O.map(element => {
      return SORT_JSON(element);
    });
  }

  return O;
}
var row = SORT_JSON(JSON.parse(json_row));
return JSON.stringify(row);
""";

CREATE OR REPLACE FUNCTION dl_service.format_ts(json_row STRING, fields ARRAY<STRING>)
  RETURNS STRING
  LANGUAGE js AS r"""
var row = JSON.parse(json_row);
for (var i in fields) {
  var field = fields[i]
  if (field in row && row[field] !== null && row[field].endsWith(".000Z")) {
    row[field] = row[field].substring(0, row[field].length - 5) + "Z";
  }
}
return JSON.stringify(row);
""";

CREATE OR REPLACE FUNCTION dl_service.delete_key(json_row STRING, fields ARRAY<STRING>)
  RETURNS STRING
  LANGUAGE js AS r"""
var row = JSON.parse(json_row);
for (var i in fields) {
  var field = fields[i]
  delete row[field]
}
return JSON.stringify(row);
""";
