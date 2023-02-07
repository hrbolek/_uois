
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 231 (class 1259 OID 57126)
-- Name: acclassificationtypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acclassificationtypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    last_change timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acclassificationtypes OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 57972)
-- Name: aclessons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aclessons (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    topic_id uuid,
    type_id uuid,
    count integer,
    last_change timestamp without time zone DEFAULT now()
);


ALTER TABLE public.aclessons OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 57135)
-- Name: aclessontypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aclessontypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    abbr character varying,
    last_change timestamp without time zone DEFAULT now()
);


ALTER TABLE public.aclessontypes OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 57056)
-- Name: acprogramforms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprogramforms (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.acprogramforms OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 57746)
-- Name: acprogramgroups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprogramgroups (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    ac_id uuid DEFAULT gen_random_uuid() NOT NULL,
    group_id uuid
);


ALTER TABLE public.acprogramgroups OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 57064)
-- Name: acprogramlanguages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprogramlanguages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.acprogramlanguages OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 57072)
-- Name: acprogramlevels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprogramlevels (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    length integer,
    priority integer
);


ALTER TABLE public.acprogramlevels OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 57762)
-- Name: acprograms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprograms (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    type_id uuid,
    last_change timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acprograms OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 57080)
-- Name: acprogramtitles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprogramtitles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.acprogramtitles OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 57406)
-- Name: acprogramtypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acprogramtypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    form_id uuid,
    language_id uuid,
    level_id uuid,
    title_id uuid
);


ALTER TABLE public.acprogramtypes OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 57941)
-- Name: acsemesters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acsemesters (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    "order" integer,
    credits integer,
    subject_id uuid,
    classificationtype_id uuid,
    last_change timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acsemesters OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 57911)
-- Name: acsubjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acsubjects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    program_id uuid,
    last_change timestamp without time zone DEFAULT now()
);


ALTER TABLE public.acsubjects OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 57958)
-- Name: actopics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actopics (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    "order" integer,
    last_change timestamp without time zone DEFAULT now(),
    semester_id uuid
);


ALTER TABLE public.actopics OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 57508)
-- Name: authorizationgroups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorizationgroups (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    authorization_id uuid NOT NULL,
    group_id uuid NOT NULL,
    accesslevel integer
);


ALTER TABLE public.authorizationgroups OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 57546)
-- Name: authorizationroletypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorizationroletypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    authorization_id uuid NOT NULL,
    group_id uuid NOT NULL,
    roletype_id uuid NOT NULL,
    accesslevel integer
);


ALTER TABLE public.authorizationroletypes OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 56993)
-- Name: authorizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorizations (
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.authorizations OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 57197)
-- Name: authorizationusers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorizationusers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    authorization_id uuid NOT NULL,
    user_id uuid NOT NULL,
    accesslevel integer
);


ALTER TABLE public.authorizationusers OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 56937)
-- Name: contents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contents (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    brief_des character varying,
    detailed_des character varying,
    event_id uuid NOT NULL
);


ALTER TABLE public.contents OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 57776)
-- Name: eventrooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventrooms (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    event_id uuid,
    facility_id uuid
);


ALTER TABLE public.eventrooms OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 57144)
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    start timestamp without time zone,
    "end" timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    eventtype_id uuid
);


ALTER TABLE public.events OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 57477)
-- Name: events_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_groups (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    event_id uuid,
    group_id uuid
);


ALTER TABLE public.events_groups OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 57445)
-- Name: events_organizers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_organizers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    event_id uuid,
    user_id uuid
);


ALTER TABLE public.events_organizers OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 57461)
-- Name: events_participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_participants (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    event_id uuid,
    user_id uuid
);


ALTER TABLE public.events_participants OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 56961)
-- Name: eventtypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eventtypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying
);


ALTER TABLE public.eventtypes OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 57340)
-- Name: externalids; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.externalids (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    typeid_id uuid,
    inner_id uuid,
    outer_id character varying
);


ALTER TABLE public.externalids OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 57040)
-- Name: externalidtypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.externalidtypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying
);


ALTER TABLE public.externalidtypes OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 66214)
-- Name: facilities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facilities (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    label character varying,
    address character varying,
    valid boolean,
    startdate timestamp without time zone,
    enddate timestamp without time zone,
    capacity integer,
    geometry character varying,
    geolocation character varying,
    lastchange timestamp without time zone DEFAULT now(),
    group_id uuid NOT NULL,
    facilitytype_id uuid,
    master_facility_id uuid
);


ALTER TABLE public.facilities OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 66241)
-- Name: facilities_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facilities_events (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    event_id uuid,
    facility_id uuid,
    state_id uuid
);


ALTER TABLE public.facilities_events OWNER TO postgres;

--
-- TOC entry 284 (class 1259 OID 66206)
-- Name: facilityeventstatetypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facilityeventstatetypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.facilityeventstatetypes OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 66198)
-- Name: facilitytypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facilitytypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying
);


ALTER TABLE public.facilitytypes OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 57925)
-- Name: formitems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formitems (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    create_at timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    "order" integer,
    value character varying,
    part_id uuid NOT NULL
);


ALTER TABLE public.formitems OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 57859)
-- Name: formparts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formparts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    create_at timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    "order" integer,
    section_id uuid NOT NULL
);


ALTER TABLE public.formparts OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 57311)
-- Name: forms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forms (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    creator_id uuid,
    create_at timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    status character varying,
    valid boolean
);


ALTER TABLE public.forms OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 57639)
-- Name: formsections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formsections (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    request_id uuid NOT NULL,
    create_at timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    "order" integer,
    status character varying
);


ALTER TABLE public.formsections OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 57158)
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groups (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    lastchange timestamp without time zone DEFAULT now(),
    "startDate" timestamp without time zone,
    "endDate" timestamp without time zone,
    valid boolean,
    grouptype_id uuid,
    mastergroup_id uuid
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 56969)
-- Name: grouptypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grouptypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.grouptypes OWNER TO postgres;

--
-- TOC entry 282 (class 1259 OID 66190)
-- Name: invitationtypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invitationtypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.invitationtypes OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 57584)
-- Name: memberships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memberships (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    group_id uuid NOT NULL,
    startdate timestamp without time zone,
    enddate timestamp without time zone,
    valid boolean
);


ALTER TABLE public.memberships OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 57016)
-- Name: personalitiesCertificateTypeGroups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesCertificateTypeGroups" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public."personalitiesCertificateTypeGroups" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 57285)
-- Name: personalitiesCertificateTypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesCertificateTypes" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    "certificateTypeGroup_id" uuid
);


ALTER TABLE public."personalitiesCertificateTypes" OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 57655)
-- Name: personalitiesCertificates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesCertificates" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    level character varying,
    validity_start timestamp without time zone,
    validity_end timestamp without time zone,
    user_id uuid,
    "certificateType_id" uuid
);


ALTER TABLE public."personalitiesCertificates" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 57024)
-- Name: personalitiesMedalTypeGroups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesMedalTypeGroups" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public."personalitiesMedalTypeGroups" OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 57298)
-- Name: personalitiesMedalTypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesMedalTypes" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    "medalTypeGroup_id" uuid
);


ALTER TABLE public."personalitiesMedalTypes" OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 57623)
-- Name: personalitiesMedals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesMedals" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    year integer,
    user_id uuid,
    "medalType_id" uuid
);


ALTER TABLE public."personalitiesMedals" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 57008)
-- Name: personalitiesRankTypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesRankTypes" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public."personalitiesRankTypes" OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 57269)
-- Name: personalitiesRanks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesRanks" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    start timestamp without time zone,
    "end" timestamp without time zone,
    user_id uuid,
    "rankType_id" uuid
);


ALTER TABLE public."personalitiesRanks" OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 57256)
-- Name: personalitiesRelatedDocs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesRelatedDocs" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    user_id uuid
);


ALTER TABLE public."personalitiesRelatedDocs" OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 57215)
-- Name: personalitiesStudies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesStudies" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    program character varying,
    start timestamp without time zone,
    "end" timestamp without time zone,
    user_id uuid
);


ALTER TABLE public."personalitiesStudies" OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 57243)
-- Name: personalitiesWorkHistories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."personalitiesWorkHistories" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    start timestamp without time zone,
    "end" timestamp without time zone,
    name character varying,
    ico character varying,
    user_id uuid
);


ALTER TABLE public."personalitiesWorkHistories" OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 56947)
-- Name: plan_lessons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_lessons (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    length integer,
    startproposal timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    linkedlesson_id uuid,
    topic_id uuid,
    lessontype_id uuid,
    semester_id uuid,
    event_id uuid
);


ALTER TABLE public.plan_lessons OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 57434)
-- Name: plan_lessons_facilities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_lessons_facilities (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    facility_id uuid,
    planlesson_id uuid
);


ALTER TABLE public.plan_lessons_facilities OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 57730)
-- Name: plan_lessons_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_lessons_groups (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    group_id uuid,
    planlesson_id uuid
);


ALTER TABLE public.plan_lessons_groups OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 57390)
-- Name: plan_lessons_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_lessons_users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    planlesson_id uuid
);


ALTER TABLE public.plan_lessons_users OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 57096)
-- Name: plan_subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_subjects (
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.plan_subjects OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 57371)
-- Name: presences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.presences (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    lastchange timestamp without time zone DEFAULT now(),
    "presenceType_id" uuid NOT NULL,
    user_id uuid NOT NULL,
    event_id uuid NOT NULL
);


ALTER TABLE public.presences OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 57048)
-- Name: presencetypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.presencetypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.presencetypes OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 57118)
-- Name: projectFinanceTypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."projectFinanceTypes" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public."projectFinanceTypes" OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 57875)
-- Name: projectFinances; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."projectFinances" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    amount numeric(13,3),
    lastchange timestamp without time zone DEFAULT now(),
    project_id uuid NOT NULL,
    "financeType_id" uuid NOT NULL
);


ALTER TABLE public."projectFinances" OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 57896)
-- Name: projectMilestones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."projectMilestones" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    startdate timestamp without time zone,
    enddate timestamp without time zone,
    project_id uuid NOT NULL
);


ALTER TABLE public."projectMilestones" OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 57102)
-- Name: projectTypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."projectTypes" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public."projectTypes" OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 57709)
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    startdate timestamp without time zone,
    enddate timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    "projectType_id" uuid NOT NULL,
    group_id uuid NOT NULL
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 57691)
-- Name: publication_authors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_authors (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    publication_id uuid NOT NULL,
    "order" integer,
    share double precision,
    lastchange timestamp without time zone
);


ALTER TABLE public.publication_authors OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 57673)
-- Name: publication_subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_subjects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    publication_id uuid NOT NULL,
    subject_id uuid NOT NULL
);


ALTER TABLE public.publication_subjects OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 57032)
-- Name: publication_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_types (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying
);


ALTER TABLE public.publication_types OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 57325)
-- Name: publications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publications (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    publication_type_id uuid NOT NULL,
    place character varying,
    published_date date,
    reference character varying,
    valid boolean,
    lastchange timestamp without time zone
);


ALTER TABLE public.publications OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 57602)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    group_id uuid,
    roletype_id uuid,
    startdate timestamp without time zone,
    enddate timestamp without time zone,
    valid boolean
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 57088)
-- Name: roletypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roletypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.roletypes OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 57526)
-- Name: surveyanswers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.surveyanswers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    value character varying,
    aswered boolean,
    expired boolean,
    user_id uuid NOT NULL,
    question_id uuid NOT NULL
);


ALTER TABLE public.surveyanswers OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 57177)
-- Name: surveyquestions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.surveyquestions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    "order" integer,
    survey_id uuid NOT NULL,
    type_id uuid NOT NULL
);


ALTER TABLE public.surveyquestions OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 56985)
-- Name: surveyquestiontypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.surveyquestiontypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying
);


ALTER TABLE public.surveyquestiontypes OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 57493)
-- Name: surveyquestionvalues; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.surveyquestionvalues (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying,
    "order" integer,
    question_id uuid NOT NULL
);


ALTER TABLE public.surveyquestionvalues OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 56977)
-- Name: surveys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.surveys (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    name_en character varying
);


ALTER TABLE public.surveys OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 57355)
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    brief_des character varying,
    detailed_des character varying,
    reference character varying,
    date_of_entry timestamp without time zone,
    date_of_submission timestamp without time zone,
    date_of_fulfillment timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now(),
    user_id uuid,
    event_id uuid
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 56999)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    surname character varying,
    email character varying,
    valid boolean,
    startdate timestamp without time zone,
    enddate timestamp without time zone,
    lastchange timestamp without time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 57228)
-- Name: workflows; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflows (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    authorization_id uuid NOT NULL
);


ALTER TABLE public.workflows OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 57839)
-- Name: workflowstateroletypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflowstateroletypes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    accesslevel integer,
    workflowstate_id uuid NOT NULL,
    roletype_id uuid NOT NULL
);


ALTER TABLE public.workflowstateroletypes OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 57569)
-- Name: workflowstates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflowstates (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    workflow_id uuid NOT NULL
);


ALTER TABLE public.workflowstates OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 57814)
-- Name: workflowstateusers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflowstateusers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying,
    accesslevel integer,
    workflowstate_id uuid NOT NULL,
    user_id uuid NOT NULL,
    group_id uuid NOT NULL
);


ALTER TABLE public.workflowstateusers OWNER TO postgres;

--
-- TOC entry 3620 (class 2606 OID 57134)
-- Name: acclassificationtypes acclassificationtypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acclassificationtypes
    ADD CONSTRAINT acclassificationtypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3770 (class 2606 OID 57978)
-- Name: aclessons aclessons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aclessons
    ADD CONSTRAINT aclessons_pkey PRIMARY KEY (id);


--
-- TOC entry 3622 (class 2606 OID 57143)
-- Name: aclessontypes aclessontypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aclessontypes
    ADD CONSTRAINT aclessontypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3604 (class 2606 OID 57063)
-- Name: acprogramforms acprogramforms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramforms
    ADD CONSTRAINT acprogramforms_pkey PRIMARY KEY (id);


--
-- TOC entry 3730 (class 2606 OID 57754)
-- Name: acprogramgroups acprogramgroups_ac_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramgroups
    ADD CONSTRAINT acprogramgroups_ac_id_key UNIQUE (ac_id);


--
-- TOC entry 3732 (class 2606 OID 57756)
-- Name: acprogramgroups acprogramgroups_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramgroups
    ADD CONSTRAINT acprogramgroups_id_key UNIQUE (id);


--
-- TOC entry 3734 (class 2606 OID 57752)
-- Name: acprogramgroups acprogramgroups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramgroups
    ADD CONSTRAINT acprogramgroups_pkey PRIMARY KEY (id, ac_id);


--
-- TOC entry 3606 (class 2606 OID 57071)
-- Name: acprogramlanguages acprogramlanguages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramlanguages
    ADD CONSTRAINT acprogramlanguages_pkey PRIMARY KEY (id);


--
-- TOC entry 3608 (class 2606 OID 57079)
-- Name: acprogramlevels acprogramlevels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramlevels
    ADD CONSTRAINT acprogramlevels_pkey PRIMARY KEY (id);


--
-- TOC entry 3736 (class 2606 OID 57770)
-- Name: acprograms acprograms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprograms
    ADD CONSTRAINT acprograms_pkey PRIMARY KEY (id);


--
-- TOC entry 3610 (class 2606 OID 57087)
-- Name: acprogramtitles acprogramtitles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramtitles
    ADD CONSTRAINT acprogramtitles_pkey PRIMARY KEY (id);


--
-- TOC entry 3672 (class 2606 OID 57413)
-- Name: acprogramtypes acprogramtypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramtypes
    ADD CONSTRAINT acprogramtypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3766 (class 2606 OID 57947)
-- Name: acsemesters acsemesters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acsemesters
    ADD CONSTRAINT acsemesters_pkey PRIMARY KEY (id);


--
-- TOC entry 3760 (class 2606 OID 57919)
-- Name: acsubjects acsubjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acsubjects
    ADD CONSTRAINT acsubjects_pkey PRIMARY KEY (id);


--
-- TOC entry 3768 (class 2606 OID 57966)
-- Name: actopics actopics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actopics
    ADD CONSTRAINT actopics_pkey PRIMARY KEY (id);


--
-- TOC entry 3686 (class 2606 OID 57515)
-- Name: authorizationgroups authorizationgroups_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationgroups
    ADD CONSTRAINT authorizationgroups_id_key UNIQUE (id);


--
-- TOC entry 3688 (class 2606 OID 57513)
-- Name: authorizationgroups authorizationgroups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationgroups
    ADD CONSTRAINT authorizationgroups_pkey PRIMARY KEY (id, authorization_id, group_id);


--
-- TOC entry 3694 (class 2606 OID 57553)
-- Name: authorizationroletypes authorizationroletypes_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationroletypes
    ADD CONSTRAINT authorizationroletypes_id_key UNIQUE (id);


--
-- TOC entry 3696 (class 2606 OID 57551)
-- Name: authorizationroletypes authorizationroletypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationroletypes
    ADD CONSTRAINT authorizationroletypes_pkey PRIMARY KEY (id, authorization_id, group_id, roletype_id);


--
-- TOC entry 3588 (class 2606 OID 56998)
-- Name: authorizations authorizations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizations
    ADD CONSTRAINT authorizations_pkey PRIMARY KEY (id);


--
-- TOC entry 3632 (class 2606 OID 57204)
-- Name: authorizationusers authorizationusers_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationusers
    ADD CONSTRAINT authorizationusers_id_key UNIQUE (id);


--
-- TOC entry 3634 (class 2606 OID 57202)
-- Name: authorizationusers authorizationusers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationusers
    ADD CONSTRAINT authorizationusers_pkey PRIMARY KEY (id, authorization_id, user_id);


--
-- TOC entry 3574 (class 2606 OID 56946)
-- Name: contents contents_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contents
    ADD CONSTRAINT contents_id_key UNIQUE (id);


--
-- TOC entry 3576 (class 2606 OID 56944)
-- Name: contents contents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contents
    ADD CONSTRAINT contents_pkey PRIMARY KEY (id, event_id);


--
-- TOC entry 3738 (class 2606 OID 57781)
-- Name: eventrooms eventrooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventrooms
    ADD CONSTRAINT eventrooms_pkey PRIMARY KEY (id);


--
-- TOC entry 3680 (class 2606 OID 57482)
-- Name: events_groups events_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_groups
    ADD CONSTRAINT events_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3676 (class 2606 OID 57450)
-- Name: events_organizers events_organizers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_organizers
    ADD CONSTRAINT events_organizers_pkey PRIMARY KEY (id);


--
-- TOC entry 3678 (class 2606 OID 57466)
-- Name: events_participants events_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_participants
    ADD CONSTRAINT events_participants_pkey PRIMARY KEY (id);


--
-- TOC entry 3624 (class 2606 OID 57152)
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- TOC entry 3580 (class 2606 OID 56968)
-- Name: eventtypes eventtypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventtypes
    ADD CONSTRAINT eventtypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3658 (class 2606 OID 57347)
-- Name: externalids externalids_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.externalids
    ADD CONSTRAINT externalids_pkey PRIMARY KEY (id);


--
-- TOC entry 3600 (class 2606 OID 57047)
-- Name: externalidtypes externalidtypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.externalidtypes
    ADD CONSTRAINT externalidtypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3783 (class 2606 OID 66246)
-- Name: facilities_events facilities_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities_events
    ADD CONSTRAINT facilities_events_pkey PRIMARY KEY (id);


--
-- TOC entry 3778 (class 2606 OID 66224)
-- Name: facilities facilities_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_id_key UNIQUE (id);


--
-- TOC entry 3780 (class 2606 OID 66222)
-- Name: facilities facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_pkey PRIMARY KEY (id, group_id);


--
-- TOC entry 3776 (class 2606 OID 66213)
-- Name: facilityeventstatetypes facilityeventstatetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilityeventstatetypes
    ADD CONSTRAINT facilityeventstatetypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3774 (class 2606 OID 66205)
-- Name: facilitytypes facilitytypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilitytypes
    ADD CONSTRAINT facilitytypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3762 (class 2606 OID 57935)
-- Name: formitems formitems_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formitems
    ADD CONSTRAINT formitems_id_key UNIQUE (id);


--
-- TOC entry 3764 (class 2606 OID 57933)
-- Name: formitems formitems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formitems
    ADD CONSTRAINT formitems_pkey PRIMARY KEY (id, part_id);


--
-- TOC entry 3748 (class 2606 OID 57869)
-- Name: formparts formparts_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formparts
    ADD CONSTRAINT formparts_id_key UNIQUE (id);


--
-- TOC entry 3750 (class 2606 OID 57867)
-- Name: formparts formparts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formparts
    ADD CONSTRAINT formparts_pkey PRIMARY KEY (id, section_id);


--
-- TOC entry 3652 (class 2606 OID 57319)
-- Name: forms forms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forms
    ADD CONSTRAINT forms_pkey PRIMARY KEY (id);


--
-- TOC entry 3710 (class 2606 OID 57649)
-- Name: formsections formsections_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formsections
    ADD CONSTRAINT formsections_id_key UNIQUE (id);


--
-- TOC entry 3712 (class 2606 OID 57647)
-- Name: formsections formsections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formsections
    ADD CONSTRAINT formsections_pkey PRIMARY KEY (id, request_id);


--
-- TOC entry 3626 (class 2606 OID 57166)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3582 (class 2606 OID 56976)
-- Name: grouptypes grouptypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grouptypes
    ADD CONSTRAINT grouptypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3772 (class 2606 OID 66197)
-- Name: invitationtypes invitationtypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invitationtypes
    ADD CONSTRAINT invitationtypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3702 (class 2606 OID 57591)
-- Name: memberships memberships_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_id_key UNIQUE (id);


--
-- TOC entry 3704 (class 2606 OID 57589)
-- Name: memberships memberships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_pkey PRIMARY KEY (id, user_id, group_id);


--
-- TOC entry 3594 (class 2606 OID 57023)
-- Name: personalitiesCertificateTypeGroups personalitiesCertificateTypeGroups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesCertificateTypeGroups"
    ADD CONSTRAINT "personalitiesCertificateTypeGroups_pkey" PRIMARY KEY (id);


--
-- TOC entry 3648 (class 2606 OID 57292)
-- Name: personalitiesCertificateTypes personalitiesCertificateTypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesCertificateTypes"
    ADD CONSTRAINT "personalitiesCertificateTypes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3714 (class 2606 OID 57662)
-- Name: personalitiesCertificates personalitiesCertificates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesCertificates"
    ADD CONSTRAINT "personalitiesCertificates_pkey" PRIMARY KEY (id);


--
-- TOC entry 3596 (class 2606 OID 57031)
-- Name: personalitiesMedalTypeGroups personalitiesMedalTypeGroups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesMedalTypeGroups"
    ADD CONSTRAINT "personalitiesMedalTypeGroups_pkey" PRIMARY KEY (id);


--
-- TOC entry 3650 (class 2606 OID 57305)
-- Name: personalitiesMedalTypes personalitiesMedalTypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesMedalTypes"
    ADD CONSTRAINT "personalitiesMedalTypes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3708 (class 2606 OID 57628)
-- Name: personalitiesMedals personalitiesMedals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesMedals"
    ADD CONSTRAINT "personalitiesMedals_pkey" PRIMARY KEY (id);


--
-- TOC entry 3592 (class 2606 OID 57015)
-- Name: personalitiesRankTypes personalitiesRankTypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesRankTypes"
    ADD CONSTRAINT "personalitiesRankTypes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3646 (class 2606 OID 57274)
-- Name: personalitiesRanks personalitiesRanks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesRanks"
    ADD CONSTRAINT "personalitiesRanks_pkey" PRIMARY KEY (id);


--
-- TOC entry 3644 (class 2606 OID 57263)
-- Name: personalitiesRelatedDocs personalitiesRelatedDocs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesRelatedDocs"
    ADD CONSTRAINT "personalitiesRelatedDocs_pkey" PRIMARY KEY (id);


--
-- TOC entry 3636 (class 2606 OID 57222)
-- Name: personalitiesStudies personalitiesStudies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesStudies"
    ADD CONSTRAINT "personalitiesStudies_pkey" PRIMARY KEY (id);


--
-- TOC entry 3642 (class 2606 OID 57250)
-- Name: personalitiesWorkHistories personalitiesWorkHistories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesWorkHistories"
    ADD CONSTRAINT "personalitiesWorkHistories_pkey" PRIMARY KEY (id);


--
-- TOC entry 3674 (class 2606 OID 57439)
-- Name: plan_lessons_facilities plan_lessons_facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_facilities
    ADD CONSTRAINT plan_lessons_facilities_pkey PRIMARY KEY (id);


--
-- TOC entry 3728 (class 2606 OID 57735)
-- Name: plan_lessons_groups plan_lessons_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_groups
    ADD CONSTRAINT plan_lessons_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3578 (class 2606 OID 56955)
-- Name: plan_lessons plan_lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons
    ADD CONSTRAINT plan_lessons_pkey PRIMARY KEY (id);


--
-- TOC entry 3670 (class 2606 OID 57395)
-- Name: plan_lessons_users plan_lessons_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_users
    ADD CONSTRAINT plan_lessons_users_pkey PRIMARY KEY (id);


--
-- TOC entry 3614 (class 2606 OID 57101)
-- Name: plan_subjects plan_subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_subjects
    ADD CONSTRAINT plan_subjects_pkey PRIMARY KEY (id);


--
-- TOC entry 3666 (class 2606 OID 57379)
-- Name: presences presences_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presences
    ADD CONSTRAINT presences_id_key UNIQUE (id);


--
-- TOC entry 3668 (class 2606 OID 57377)
-- Name: presences presences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presences
    ADD CONSTRAINT presences_pkey PRIMARY KEY (id, "presenceType_id", user_id, event_id);


--
-- TOC entry 3602 (class 2606 OID 57055)
-- Name: presencetypes presencetypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presencetypes
    ADD CONSTRAINT presencetypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3618 (class 2606 OID 57125)
-- Name: projectFinanceTypes projectFinanceTypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectFinanceTypes"
    ADD CONSTRAINT "projectFinanceTypes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3752 (class 2606 OID 57885)
-- Name: projectFinances projectFinances_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectFinances"
    ADD CONSTRAINT "projectFinances_id_key" UNIQUE (id);


--
-- TOC entry 3754 (class 2606 OID 57883)
-- Name: projectFinances projectFinances_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectFinances"
    ADD CONSTRAINT "projectFinances_pkey" PRIMARY KEY (id, project_id, "financeType_id");


--
-- TOC entry 3756 (class 2606 OID 57905)
-- Name: projectMilestones projectMilestones_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectMilestones"
    ADD CONSTRAINT "projectMilestones_id_key" UNIQUE (id);


--
-- TOC entry 3758 (class 2606 OID 57903)
-- Name: projectMilestones projectMilestones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectMilestones"
    ADD CONSTRAINT "projectMilestones_pkey" PRIMARY KEY (id, project_id);


--
-- TOC entry 3616 (class 2606 OID 57109)
-- Name: projectTypes projectTypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectTypes"
    ADD CONSTRAINT "projectTypes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3724 (class 2606 OID 57719)
-- Name: projects projects_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_id_key UNIQUE (id);


--
-- TOC entry 3726 (class 2606 OID 57717)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id, "projectType_id", group_id);


--
-- TOC entry 3720 (class 2606 OID 57698)
-- Name: publication_authors publication_authors_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_authors
    ADD CONSTRAINT publication_authors_id_key UNIQUE (id);


--
-- TOC entry 3722 (class 2606 OID 57696)
-- Name: publication_authors publication_authors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_authors
    ADD CONSTRAINT publication_authors_pkey PRIMARY KEY (id, user_id, publication_id);


--
-- TOC entry 3716 (class 2606 OID 57680)
-- Name: publication_subjects publication_subjects_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_subjects
    ADD CONSTRAINT publication_subjects_id_key UNIQUE (id);


--
-- TOC entry 3718 (class 2606 OID 57678)
-- Name: publication_subjects publication_subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_subjects
    ADD CONSTRAINT publication_subjects_pkey PRIMARY KEY (id, publication_id, subject_id);


--
-- TOC entry 3598 (class 2606 OID 57039)
-- Name: publication_types publication_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_types
    ADD CONSTRAINT publication_types_pkey PRIMARY KEY (id);


--
-- TOC entry 3654 (class 2606 OID 57334)
-- Name: publications publications_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_id_key UNIQUE (id);


--
-- TOC entry 3656 (class 2606 OID 57332)
-- Name: publications publications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_pkey PRIMARY KEY (id, publication_type_id);


--
-- TOC entry 3706 (class 2606 OID 57607)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3612 (class 2606 OID 57095)
-- Name: roletypes roletypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roletypes
    ADD CONSTRAINT roletypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3690 (class 2606 OID 57535)
-- Name: surveyanswers surveyanswers_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyanswers
    ADD CONSTRAINT surveyanswers_id_key UNIQUE (id);


--
-- TOC entry 3692 (class 2606 OID 57533)
-- Name: surveyanswers surveyanswers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyanswers
    ADD CONSTRAINT surveyanswers_pkey PRIMARY KEY (id, user_id, question_id);


--
-- TOC entry 3628 (class 2606 OID 57186)
-- Name: surveyquestions surveyquestions_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestions
    ADD CONSTRAINT surveyquestions_id_key UNIQUE (id);


--
-- TOC entry 3630 (class 2606 OID 57184)
-- Name: surveyquestions surveyquestions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestions
    ADD CONSTRAINT surveyquestions_pkey PRIMARY KEY (id, survey_id, type_id);


--
-- TOC entry 3586 (class 2606 OID 56992)
-- Name: surveyquestiontypes surveyquestiontypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestiontypes
    ADD CONSTRAINT surveyquestiontypes_pkey PRIMARY KEY (id);


--
-- TOC entry 3682 (class 2606 OID 57502)
-- Name: surveyquestionvalues surveyquestionvalues_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestionvalues
    ADD CONSTRAINT surveyquestionvalues_id_key UNIQUE (id);


--
-- TOC entry 3684 (class 2606 OID 57500)
-- Name: surveyquestionvalues surveyquestionvalues_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestionvalues
    ADD CONSTRAINT surveyquestionvalues_pkey PRIMARY KEY (id, question_id);


--
-- TOC entry 3584 (class 2606 OID 56984)
-- Name: surveys surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveys
    ADD CONSTRAINT surveys_pkey PRIMARY KEY (id);


--
-- TOC entry 3664 (class 2606 OID 57363)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3590 (class 2606 OID 57007)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3638 (class 2606 OID 57237)
-- Name: workflows workflows_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_id_key UNIQUE (id);


--
-- TOC entry 3640 (class 2606 OID 57235)
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id, authorization_id);


--
-- TOC entry 3744 (class 2606 OID 57848)
-- Name: workflowstateroletypes workflowstateroletypes_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateroletypes
    ADD CONSTRAINT workflowstateroletypes_id_key UNIQUE (id);


--
-- TOC entry 3746 (class 2606 OID 57846)
-- Name: workflowstateroletypes workflowstateroletypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateroletypes
    ADD CONSTRAINT workflowstateroletypes_pkey PRIMARY KEY (id, workflowstate_id, roletype_id);


--
-- TOC entry 3698 (class 2606 OID 57578)
-- Name: workflowstates workflowstates_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstates
    ADD CONSTRAINT workflowstates_id_key UNIQUE (id);


--
-- TOC entry 3700 (class 2606 OID 57576)
-- Name: workflowstates workflowstates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstates
    ADD CONSTRAINT workflowstates_pkey PRIMARY KEY (id, workflow_id);


--
-- TOC entry 3740 (class 2606 OID 57823)
-- Name: workflowstateusers workflowstateusers_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateusers
    ADD CONSTRAINT workflowstateusers_id_key UNIQUE (id);


--
-- TOC entry 3742 (class 2606 OID 57821)
-- Name: workflowstateusers workflowstateusers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateusers
    ADD CONSTRAINT workflowstateusers_pkey PRIMARY KEY (id, workflowstate_id, user_id, group_id);


--
-- TOC entry 3659 (class 1259 OID 57354)
-- Name: ix_externalids_inner_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_externalids_inner_id ON public.externalids USING btree (inner_id);


--
-- TOC entry 3660 (class 1259 OID 57353)
-- Name: ix_externalids_outer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_externalids_outer_id ON public.externalids USING btree (outer_id);


--
-- TOC entry 3781 (class 1259 OID 66240)
-- Name: ix_facilities_master_facility_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_facilities_master_facility_id ON public.facilities USING btree (master_facility_id);


--
-- TOC entry 3661 (class 1259 OID 57369)
-- Name: ix_tasks_event_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_event_id ON public.tasks USING btree (event_id);


--
-- TOC entry 3662 (class 1259 OID 57370)
-- Name: ix_tasks_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_user_id ON public.tasks USING btree (user_id);


--
-- TOC entry 3863 (class 2606 OID 57979)
-- Name: aclessons aclessons_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aclessons
    ADD CONSTRAINT aclessons_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.actopics(id);


--
-- TOC entry 3864 (class 2606 OID 57984)
-- Name: aclessons aclessons_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aclessons
    ADD CONSTRAINT aclessons_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.aclessontypes(id);


--
-- TOC entry 3846 (class 2606 OID 57757)
-- Name: acprogramgroups acprogramgroups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramgroups
    ADD CONSTRAINT acprogramgroups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3847 (class 2606 OID 57771)
-- Name: acprograms acprograms_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprograms
    ADD CONSTRAINT acprograms_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.acprogramtypes(id);


--
-- TOC entry 3808 (class 2606 OID 57414)
-- Name: acprogramtypes acprogramtypes_form_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramtypes
    ADD CONSTRAINT acprogramtypes_form_id_fkey FOREIGN KEY (form_id) REFERENCES public.acprogramforms(id);


--
-- TOC entry 3809 (class 2606 OID 57419)
-- Name: acprogramtypes acprogramtypes_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramtypes
    ADD CONSTRAINT acprogramtypes_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.acprogramlanguages(id);


--
-- TOC entry 3810 (class 2606 OID 57424)
-- Name: acprogramtypes acprogramtypes_level_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramtypes
    ADD CONSTRAINT acprogramtypes_level_id_fkey FOREIGN KEY (level_id) REFERENCES public.acprogramlevels(id);


--
-- TOC entry 3811 (class 2606 OID 57429)
-- Name: acprogramtypes acprogramtypes_title_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acprogramtypes
    ADD CONSTRAINT acprogramtypes_title_id_fkey FOREIGN KEY (title_id) REFERENCES public.acprogramtitles(id);


--
-- TOC entry 3860 (class 2606 OID 57948)
-- Name: acsemesters acsemesters_classificationtype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acsemesters
    ADD CONSTRAINT acsemesters_classificationtype_id_fkey FOREIGN KEY (classificationtype_id) REFERENCES public.acclassificationtypes(id);


--
-- TOC entry 3861 (class 2606 OID 57953)
-- Name: acsemesters acsemesters_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acsemesters
    ADD CONSTRAINT acsemesters_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.acsubjects(id);


--
-- TOC entry 3858 (class 2606 OID 57920)
-- Name: acsubjects acsubjects_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acsubjects
    ADD CONSTRAINT acsubjects_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.acprograms(id);


--
-- TOC entry 3862 (class 2606 OID 57967)
-- Name: actopics actopics_semester_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actopics
    ADD CONSTRAINT actopics_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES public.acsemesters(id);


--
-- TOC entry 3820 (class 2606 OID 57516)
-- Name: authorizationgroups authorizationgroups_authorization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationgroups
    ADD CONSTRAINT authorizationgroups_authorization_id_fkey FOREIGN KEY (authorization_id) REFERENCES public.authorizations(id);


--
-- TOC entry 3821 (class 2606 OID 57521)
-- Name: authorizationgroups authorizationgroups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationgroups
    ADD CONSTRAINT authorizationgroups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3824 (class 2606 OID 57554)
-- Name: authorizationroletypes authorizationroletypes_authorization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationroletypes
    ADD CONSTRAINT authorizationroletypes_authorization_id_fkey FOREIGN KEY (authorization_id) REFERENCES public.authorizations(id);


--
-- TOC entry 3825 (class 2606 OID 57559)
-- Name: authorizationroletypes authorizationroletypes_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationroletypes
    ADD CONSTRAINT authorizationroletypes_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3826 (class 2606 OID 57564)
-- Name: authorizationroletypes authorizationroletypes_roletype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationroletypes
    ADD CONSTRAINT authorizationroletypes_roletype_id_fkey FOREIGN KEY (roletype_id) REFERENCES public.roletypes(id);


--
-- TOC entry 3790 (class 2606 OID 57205)
-- Name: authorizationusers authorizationusers_authorization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationusers
    ADD CONSTRAINT authorizationusers_authorization_id_fkey FOREIGN KEY (authorization_id) REFERENCES public.authorizations(id);


--
-- TOC entry 3791 (class 2606 OID 57210)
-- Name: authorizationusers authorizationusers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorizationusers
    ADD CONSTRAINT authorizationusers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3848 (class 2606 OID 57782)
-- Name: eventrooms eventrooms_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eventrooms
    ADD CONSTRAINT eventrooms_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- TOC entry 3785 (class 2606 OID 57153)
-- Name: events events_eventtype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_eventtype_id_fkey FOREIGN KEY (eventtype_id) REFERENCES public.eventtypes(id);


--
-- TOC entry 3817 (class 2606 OID 57483)
-- Name: events_groups events_groups_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_groups
    ADD CONSTRAINT events_groups_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- TOC entry 3818 (class 2606 OID 57488)
-- Name: events_groups events_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_groups
    ADD CONSTRAINT events_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3813 (class 2606 OID 57451)
-- Name: events_organizers events_organizers_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_organizers
    ADD CONSTRAINT events_organizers_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- TOC entry 3814 (class 2606 OID 57456)
-- Name: events_organizers events_organizers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_organizers
    ADD CONSTRAINT events_organizers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3815 (class 2606 OID 57467)
-- Name: events_participants events_participants_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_participants
    ADD CONSTRAINT events_participants_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- TOC entry 3816 (class 2606 OID 57472)
-- Name: events_participants events_participants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_participants
    ADD CONSTRAINT events_participants_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3802 (class 2606 OID 57348)
-- Name: externalids externalids_typeid_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.externalids
    ADD CONSTRAINT externalids_typeid_id_fkey FOREIGN KEY (typeid_id) REFERENCES public.externalidtypes(id);


--
-- TOC entry 3868 (class 2606 OID 66247)
-- Name: facilities_events facilities_events_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities_events
    ADD CONSTRAINT facilities_events_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- TOC entry 3869 (class 2606 OID 66252)
-- Name: facilities_events facilities_events_facility_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities_events
    ADD CONSTRAINT facilities_events_facility_id_fkey FOREIGN KEY (facility_id) REFERENCES public.facilities(id);


--
-- TOC entry 3870 (class 2606 OID 66257)
-- Name: facilities_events facilities_events_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities_events
    ADD CONSTRAINT facilities_events_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.facilityeventstatetypes(id);


--
-- TOC entry 3865 (class 2606 OID 66230)
-- Name: facilities facilities_facilitytype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_facilitytype_id_fkey FOREIGN KEY (facilitytype_id) REFERENCES public.facilitytypes(id);


--
-- TOC entry 3866 (class 2606 OID 66225)
-- Name: facilities facilities_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3867 (class 2606 OID 66235)
-- Name: facilities facilities_master_facility_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facilities
    ADD CONSTRAINT facilities_master_facility_id_fkey FOREIGN KEY (master_facility_id) REFERENCES public.facilities(id);


--
-- TOC entry 3859 (class 2606 OID 57936)
-- Name: formitems formitems_part_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formitems
    ADD CONSTRAINT formitems_part_id_fkey FOREIGN KEY (part_id) REFERENCES public.formparts(id);


--
-- TOC entry 3854 (class 2606 OID 57870)
-- Name: formparts formparts_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formparts
    ADD CONSTRAINT formparts_section_id_fkey FOREIGN KEY (section_id) REFERENCES public.formsections(id);


--
-- TOC entry 3800 (class 2606 OID 57320)
-- Name: forms forms_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forms
    ADD CONSTRAINT forms_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- TOC entry 3835 (class 2606 OID 57650)
-- Name: formsections formsections_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formsections
    ADD CONSTRAINT formsections_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.forms(id);


--
-- TOC entry 3786 (class 2606 OID 57167)
-- Name: groups groups_grouptype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_grouptype_id_fkey FOREIGN KEY (grouptype_id) REFERENCES public.grouptypes(id);


--
-- TOC entry 3787 (class 2606 OID 57172)
-- Name: groups groups_mastergroup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_mastergroup_id_fkey FOREIGN KEY (mastergroup_id) REFERENCES public.groups(id);


--
-- TOC entry 3828 (class 2606 OID 57592)
-- Name: memberships memberships_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3829 (class 2606 OID 57597)
-- Name: memberships memberships_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3798 (class 2606 OID 57293)
-- Name: personalitiesCertificateTypes personalitiesCertificateTypes_certificateTypeGroup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesCertificateTypes"
    ADD CONSTRAINT "personalitiesCertificateTypes_certificateTypeGroup_id_fkey" FOREIGN KEY ("certificateTypeGroup_id") REFERENCES public."personalitiesCertificateTypeGroups"(id);


--
-- TOC entry 3836 (class 2606 OID 57663)
-- Name: personalitiesCertificates personalitiesCertificates_certificateType_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesCertificates"
    ADD CONSTRAINT "personalitiesCertificates_certificateType_id_fkey" FOREIGN KEY ("certificateType_id") REFERENCES public."personalitiesCertificateTypes"(id);


--
-- TOC entry 3837 (class 2606 OID 57668)
-- Name: personalitiesCertificates personalitiesCertificates_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesCertificates"
    ADD CONSTRAINT "personalitiesCertificates_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3799 (class 2606 OID 57306)
-- Name: personalitiesMedalTypes personalitiesMedalTypes_medalTypeGroup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesMedalTypes"
    ADD CONSTRAINT "personalitiesMedalTypes_medalTypeGroup_id_fkey" FOREIGN KEY ("medalTypeGroup_id") REFERENCES public."personalitiesMedalTypeGroups"(id);


--
-- TOC entry 3833 (class 2606 OID 57629)
-- Name: personalitiesMedals personalitiesMedals_medalType_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesMedals"
    ADD CONSTRAINT "personalitiesMedals_medalType_id_fkey" FOREIGN KEY ("medalType_id") REFERENCES public."personalitiesMedalTypes"(id);


--
-- TOC entry 3834 (class 2606 OID 57634)
-- Name: personalitiesMedals personalitiesMedals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesMedals"
    ADD CONSTRAINT "personalitiesMedals_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3796 (class 2606 OID 57275)
-- Name: personalitiesRanks personalitiesRanks_rankType_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesRanks"
    ADD CONSTRAINT "personalitiesRanks_rankType_id_fkey" FOREIGN KEY ("rankType_id") REFERENCES public."personalitiesRankTypes"(id);


--
-- TOC entry 3797 (class 2606 OID 57280)
-- Name: personalitiesRanks personalitiesRanks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesRanks"
    ADD CONSTRAINT "personalitiesRanks_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3795 (class 2606 OID 57264)
-- Name: personalitiesRelatedDocs personalitiesRelatedDocs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesRelatedDocs"
    ADD CONSTRAINT "personalitiesRelatedDocs_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3792 (class 2606 OID 57223)
-- Name: personalitiesStudies personalitiesStudies_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesStudies"
    ADD CONSTRAINT "personalitiesStudies_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3794 (class 2606 OID 57251)
-- Name: personalitiesWorkHistories personalitiesWorkHistories_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."personalitiesWorkHistories"
    ADD CONSTRAINT "personalitiesWorkHistories_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3812 (class 2606 OID 57440)
-- Name: plan_lessons_facilities plan_lessons_facilities_planlesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_facilities
    ADD CONSTRAINT plan_lessons_facilities_planlesson_id_fkey FOREIGN KEY (planlesson_id) REFERENCES public.plan_lessons(id);


--
-- TOC entry 3844 (class 2606 OID 57736)
-- Name: plan_lessons_groups plan_lessons_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_groups
    ADD CONSTRAINT plan_lessons_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3845 (class 2606 OID 57741)
-- Name: plan_lessons_groups plan_lessons_groups_planlesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_groups
    ADD CONSTRAINT plan_lessons_groups_planlesson_id_fkey FOREIGN KEY (planlesson_id) REFERENCES public.plan_lessons(id);


--
-- TOC entry 3784 (class 2606 OID 56956)
-- Name: plan_lessons plan_lessons_linkedlesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons
    ADD CONSTRAINT plan_lessons_linkedlesson_id_fkey FOREIGN KEY (linkedlesson_id) REFERENCES public.plan_lessons(id);


--
-- TOC entry 3806 (class 2606 OID 57396)
-- Name: plan_lessons_users plan_lessons_users_planlesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_users
    ADD CONSTRAINT plan_lessons_users_planlesson_id_fkey FOREIGN KEY (planlesson_id) REFERENCES public.plan_lessons(id);


--
-- TOC entry 3807 (class 2606 OID 57401)
-- Name: plan_lessons_users plan_lessons_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_lessons_users
    ADD CONSTRAINT plan_lessons_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3804 (class 2606 OID 57380)
-- Name: presences presences_presenceType_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presences
    ADD CONSTRAINT "presences_presenceType_id_fkey" FOREIGN KEY ("presenceType_id") REFERENCES public.presencetypes(id);


--
-- TOC entry 3805 (class 2606 OID 57385)
-- Name: presences presences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.presences
    ADD CONSTRAINT presences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3855 (class 2606 OID 57886)
-- Name: projectFinances projectFinances_financeType_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectFinances"
    ADD CONSTRAINT "projectFinances_financeType_id_fkey" FOREIGN KEY ("financeType_id") REFERENCES public."projectFinanceTypes"(id);


--
-- TOC entry 3856 (class 2606 OID 57891)
-- Name: projectFinances projectFinances_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectFinances"
    ADD CONSTRAINT "projectFinances_project_id_fkey" FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- TOC entry 3857 (class 2606 OID 57906)
-- Name: projectMilestones projectMilestones_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."projectMilestones"
    ADD CONSTRAINT "projectMilestones_project_id_fkey" FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- TOC entry 3842 (class 2606 OID 57720)
-- Name: projects projects_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3843 (class 2606 OID 57725)
-- Name: projects projects_projectType_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT "projects_projectType_id_fkey" FOREIGN KEY ("projectType_id") REFERENCES public."projectTypes"(id);


--
-- TOC entry 3840 (class 2606 OID 57699)
-- Name: publication_authors publication_authors_publication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_authors
    ADD CONSTRAINT publication_authors_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES public.publications(id);


--
-- TOC entry 3841 (class 2606 OID 57704)
-- Name: publication_authors publication_authors_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_authors
    ADD CONSTRAINT publication_authors_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3838 (class 2606 OID 57681)
-- Name: publication_subjects publication_subjects_publication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_subjects
    ADD CONSTRAINT publication_subjects_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES public.publications(id);


--
-- TOC entry 3839 (class 2606 OID 57686)
-- Name: publication_subjects publication_subjects_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_subjects
    ADD CONSTRAINT publication_subjects_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.plan_subjects(id);


--
-- TOC entry 3801 (class 2606 OID 57335)
-- Name: publications publications_publication_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_publication_type_id_fkey FOREIGN KEY (publication_type_id) REFERENCES public.publication_types(id);


--
-- TOC entry 3830 (class 2606 OID 57608)
-- Name: roles roles_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3831 (class 2606 OID 57613)
-- Name: roles roles_roletype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_roletype_id_fkey FOREIGN KEY (roletype_id) REFERENCES public.roletypes(id);


--
-- TOC entry 3832 (class 2606 OID 57618)
-- Name: roles roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3822 (class 2606 OID 57536)
-- Name: surveyanswers surveyanswers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyanswers
    ADD CONSTRAINT surveyanswers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.surveyquestions(id);


--
-- TOC entry 3823 (class 2606 OID 57541)
-- Name: surveyanswers surveyanswers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyanswers
    ADD CONSTRAINT surveyanswers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3788 (class 2606 OID 57187)
-- Name: surveyquestions surveyquestions_survey_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestions
    ADD CONSTRAINT surveyquestions_survey_id_fkey FOREIGN KEY (survey_id) REFERENCES public.surveys(id);


--
-- TOC entry 3789 (class 2606 OID 57192)
-- Name: surveyquestions surveyquestions_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestions
    ADD CONSTRAINT surveyquestions_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.surveyquestiontypes(id);


--
-- TOC entry 3819 (class 2606 OID 57503)
-- Name: surveyquestionvalues surveyquestionvalues_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.surveyquestionvalues
    ADD CONSTRAINT surveyquestionvalues_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.surveyquestions(id);


--
-- TOC entry 3803 (class 2606 OID 57364)
-- Name: tasks tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3793 (class 2606 OID 57238)
-- Name: workflows workflows_authorization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_authorization_id_fkey FOREIGN KEY (authorization_id) REFERENCES public.authorizations(id);


--
-- TOC entry 3852 (class 2606 OID 57849)
-- Name: workflowstateroletypes workflowstateroletypes_roletype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateroletypes
    ADD CONSTRAINT workflowstateroletypes_roletype_id_fkey FOREIGN KEY (roletype_id) REFERENCES public.roletypes(id);


--
-- TOC entry 3853 (class 2606 OID 57854)
-- Name: workflowstateroletypes workflowstateroletypes_workflowstate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateroletypes
    ADD CONSTRAINT workflowstateroletypes_workflowstate_id_fkey FOREIGN KEY (workflowstate_id) REFERENCES public.workflowstates(id);


--
-- TOC entry 3827 (class 2606 OID 57579)
-- Name: workflowstates workflowstates_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstates
    ADD CONSTRAINT workflowstates_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES public.workflows(id);


--
-- TOC entry 3849 (class 2606 OID 57824)
-- Name: workflowstateusers workflowstateusers_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateusers
    ADD CONSTRAINT workflowstateusers_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- TOC entry 3850 (class 2606 OID 57829)
-- Name: workflowstateusers workflowstateusers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateusers
    ADD CONSTRAINT workflowstateusers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3851 (class 2606 OID 57834)
-- Name: workflowstateusers workflowstateusers_workflowstate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflowstateusers
    ADD CONSTRAINT workflowstateusers_workflowstate_id_fkey FOREIGN KEY (workflowstate_id) REFERENCES public.workflowstates(id);


--
-- TOC entry 4015 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2023-02-07 17:42:17 UTC

--
-- PostgreSQL database dump complete
--
