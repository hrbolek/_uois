-- schema_local_db.sql
-- Local_DB schema for Decree 53 §17 compliance
-- Must be stored within Vietnam: user relationship data + IP logs

CREATE TABLE IF NOT EXISTS ip_logs (
    id            CHAR(36)     NOT NULL PRIMARY KEY,
    user_id       CHAR(36)     NULL,
    ip_address    VARCHAR(45)  NOT NULL,
    endpoint      VARCHAR(512) NOT NULL,
    method        VARCHAR(10)  NOT NULL,
    user_agent    VARCHAR(512) NULL,
    gql_operation VARCHAR(255) NULL,
    status_code   SMALLINT     NOT NULL,
    data_category VARCHAR(50)  NOT NULL,   -- user_profile | app_metadata | image_cache
    ts            DATETIME     NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_profile_audit (
    id             CHAR(36)     NOT NULL PRIMARY KEY,
    user_id        CHAR(36)     NULL,
    operation_name VARCHAR(255) NULL,
    payload        MEDIUMTEXT   NOT NULL,  -- JSON: {query, variables}
    recorded_at    DATETIME     NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mirror: users (field names verified against systemdata.hk2026.json)
CREATE TABLE IF NOT EXISTS users_mirror (
    id          CHAR(36)     NOT NULL PRIMARY KEY,
    name        VARCHAR(255) NULL,
    firstname   VARCHAR(255) NULL,
    familyname  VARCHAR(255) NULL,
    surname     VARCHAR(255) NULL,
    email       VARCHAR(255) NULL,
    created     DATETIME     NULL,
    lastchange  DATETIME     NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mirror: groups (note: field is "abbr", NOT "abbreviation")
CREATE TABLE IF NOT EXISTS groups_mirror (
    id             CHAR(36)     NOT NULL PRIMARY KEY,
    name           VARCHAR(255) NULL,
    abbr           VARCHAR(64)  NULL,
    grouptype_id   CHAR(36)     NULL,
    mastergroup_id CHAR(36)     NULL,
    created        DATETIME     NULL,
    lastchange     DATETIME     NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mirror: memberships (note: NO startdate/enddate fields)
CREATE TABLE IF NOT EXISTS memberships_mirror (
    id         CHAR(36) NOT NULL PRIMARY KEY,
    user_id    CHAR(36) NULL,
    group_id   CHAR(36) NULL,
    valid      TINYINT  NULL,
    created    DATETIME NULL,
    lastchange DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mirror: roles
CREATE TABLE IF NOT EXISTS roles_mirror (
    id          CHAR(36) NOT NULL PRIMARY KEY,
    user_id     CHAR(36) NULL,
    group_id    CHAR(36) NULL,
    roletype_id CHAR(36) NULL,
    valid       TINYINT  NULL,
    startdate   DATETIME NULL,
    enddate     DATETIME NULL,
    createdby   CHAR(36) NULL,
    changedby   CHAR(36) NULL,
    created     DATETIME NULL,
    lastchange  DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mirror: roletypes
CREATE TABLE IF NOT EXISTS roletypes_mirror (
    id          CHAR(36)     NOT NULL PRIMARY KEY,
    name        VARCHAR(255) NULL,
    name_en     VARCHAR(255) NULL,
    category_id CHAR(36)     NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mirror: grouptypes
CREATE TABLE IF NOT EXISTS grouptypes_mirror (
    id          CHAR(36)     NOT NULL PRIMARY KEY,
    name        VARCHAR(255) NULL,
    name_en     VARCHAR(255) NULL,
    ex_type     VARCHAR(64)  NULL,
    category_id CHAR(36)     NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
