--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.5
-- Dumped by pg_dump version 9.4.5
-- Started on 2017-04-14 10:29:55 IST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 10 (class 2615 OID 58630)
-- Name: talentspear_auth; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA talentspear_auth;


ALTER SCHEMA talentspear_auth OWNER TO postgres;

SET search_path = talentspear_auth, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 259 (class 1259 OID 58646)
-- Name: CLIENT; Type: TABLE; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

CREATE TABLE "CLIENT" (
    "CLIENT_ID" text NOT NULL,
    "USER_ID" integer,
    "CLIENT_SECRET" text,
    "DEFAULT_SCOPES" text,
    "REDIRECT_URIS" text
);


ALTER TABLE "CLIENT" OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 58633)
-- Name: grant_id_sequence; Type: SEQUENCE; Schema: talentspear_auth; Owner: postgres
--

CREATE SEQUENCE grant_id_sequence
    START WITH 101
    INCREMENT BY 1
    MINVALUE 100
    MAXVALUE 999999999999999999
    CACHE 1;


ALTER TABLE grant_id_sequence OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 58659)
-- Name: GRANT; Type: TABLE; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

CREATE TABLE "GRANT" (
    "GRANT_ID" integer DEFAULT nextval('grant_id_sequence'::regclass) NOT NULL,
    "USER_ID" integer,
    "CLIENT_ID" text,
    "CODE" text NOT NULL,
    "REDIRECT_URI" text,
    "SCOPES" text,
    "EXPIRES" timestamp with time zone
);


ALTER TABLE "GRANT" OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 58635)
-- Name: token_id_sequence; Type: SEQUENCE; Schema: talentspear_auth; Owner: postgres
--

CREATE SEQUENCE token_id_sequence
    START WITH 101
    INCREMENT BY 1
    MINVALUE 100
    MAXVALUE 999999999999999999
    CACHE 1;


ALTER TABLE token_id_sequence OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 58679)
-- Name: TOKEN; Type: TABLE; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

CREATE TABLE "TOKEN" (
    "TOKEN_ID" integer DEFAULT nextval('token_id_sequence'::regclass) NOT NULL,
    "USER_ID" integer,
    "CLIENT_ID" text,
    "TOKEN_TYPE" text,
    "ACCESS_TOKEN" text,
    "REFRESH_TOKEN" text,
    "EXPIRES" timestamp with time zone,
    "SCOPES" text
);


ALTER TABLE "TOKEN" OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 58631)
-- Name: user_id_sequence; Type: SEQUENCE; Schema: talentspear_auth; Owner: postgres
--

CREATE SEQUENCE user_id_sequence
    START WITH 101
    INCREMENT BY 1
    MINVALUE 100
    MAXVALUE 999999999999999999
    CACHE 1;


ALTER TABLE user_id_sequence OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 58637)
-- Name: USER_TABLE; Type: TABLE; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

CREATE TABLE "USER_TABLE" (
    "USER_ID" integer DEFAULT nextval('user_id_sequence'::regclass) NOT NULL,
    "USERNAME" text
);


ALTER TABLE "USER_TABLE" OWNER TO postgres;

--
-- TOC entry 2209 (class 2606 OID 58714)
-- Name: CLIENT_USER_ID_key; Type: CONSTRAINT; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "CLIENT"
    ADD CONSTRAINT "CLIENT_USER_ID_key" UNIQUE ("USER_ID");


--
-- TOC entry 2211 (class 2606 OID 58653)
-- Name: CLIENT_pkey; Type: CONSTRAINT; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "CLIENT"
    ADD CONSTRAINT "CLIENT_pkey" PRIMARY KEY ("CLIENT_ID");


--
-- TOC entry 2213 (class 2606 OID 58691)
-- Name: TOKEN_pkey; Type: CONSTRAINT; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "TOKEN"
    ADD CONSTRAINT "TOKEN_pkey" PRIMARY KEY ("TOKEN_ID");


--
-- TOC entry 2207 (class 2606 OID 58642)
-- Name: pk_id_USER_TABLE; Type: CONSTRAINT; Schema: talentspear_auth; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "USER_TABLE"
    ADD CONSTRAINT "pk_id_USER_TABLE" PRIMARY KEY ("USER_ID");


--
-- TOC entry 2214 (class 2606 OID 58654)
-- Name: CLIENT_USER_ID_fkey; Type: FK CONSTRAINT; Schema: talentspear_auth; Owner: postgres
--

ALTER TABLE ONLY "CLIENT"
    ADD CONSTRAINT "CLIENT_USER_ID_fkey" FOREIGN KEY ("USER_ID") REFERENCES "USER_TABLE"("USER_ID");


--
-- TOC entry 2215 (class 2606 OID 58669)
-- Name: GRANT_CLIENT_ID_fkey; Type: FK CONSTRAINT; Schema: talentspear_auth; Owner: postgres
--

ALTER TABLE ONLY "GRANT"
    ADD CONSTRAINT "GRANT_CLIENT_ID_fkey" FOREIGN KEY ("CLIENT_ID") REFERENCES "CLIENT"("CLIENT_ID");


--
-- TOC entry 2216 (class 2606 OID 58674)
-- Name: GRANT_USER_ID_fkey; Type: FK CONSTRAINT; Schema: talentspear_auth; Owner: postgres
--

ALTER TABLE ONLY "GRANT"
    ADD CONSTRAINT "GRANT_USER_ID_fkey" FOREIGN KEY ("USER_ID") REFERENCES "USER_TABLE"("USER_ID");


--
-- TOC entry 2217 (class 2606 OID 58692)
-- Name: TOKEN_CLIENT_ID_fkey; Type: FK CONSTRAINT; Schema: talentspear_auth; Owner: postgres
--

ALTER TABLE ONLY "TOKEN"
    ADD CONSTRAINT "TOKEN_CLIENT_ID_fkey" FOREIGN KEY ("CLIENT_ID") REFERENCES "CLIENT"("CLIENT_ID");


--
-- TOC entry 2218 (class 2606 OID 58697)
-- Name: TOKEN_USER_ID_fkey; Type: FK CONSTRAINT; Schema: talentspear_auth; Owner: postgres
--

ALTER TABLE ONLY "TOKEN"
    ADD CONSTRAINT "TOKEN_USER_ID_fkey" FOREIGN KEY ("USER_ID") REFERENCES "USER_TABLE"("USER_ID");


-- Completed on 2017-04-14 10:29:56 IST

--
-- PostgreSQL database dump complete
--

