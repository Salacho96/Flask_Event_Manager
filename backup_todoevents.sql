--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

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

--
-- Name: eventstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.eventstatus AS ENUM (
    'DRAFT',
    'PUBLISHED',
    'CANCELLED'
);


ALTER TYPE public.eventstatus OWNER TO postgres;

--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roleenum AS ENUM (
    'ADMIN',
    'ORGANIZER',
    'ATTENDEE'
);


ALTER TYPE public.roleenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: attendee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendee (
    user_id integer NOT NULL,
    event_id integer NOT NULL,
    session_id integer,
    created_at timestamp without time zone
);


ALTER TABLE public.attendee OWNER TO postgres;

--
-- Name: event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.event (
    id integer NOT NULL,
    name character varying(180),
    description text,
    capacity integer,
    registered integer,
    status public.eventstatus,
    start_at timestamp without time zone,
    end_at timestamp without time zone,
    created_by_id integer,
    created_at timestamp without time zone
);


ALTER TABLE public.event OWNER TO postgres;

--
-- Name: event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.event_id_seq OWNER TO postgres;

--
-- Name: event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.event_id_seq OWNED BY public.event.id;


--
-- Name: session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.session (
    id integer NOT NULL,
    event_id integer NOT NULL,
    title character varying(180) NOT NULL,
    speaker character varying(180),
    start_at timestamp without time zone NOT NULL,
    end_at timestamp without time zone NOT NULL,
    capacity integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.session OWNER TO postgres;

--
-- Name: session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.session_id_seq OWNER TO postgres;

--
-- Name: session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.session_id_seq OWNED BY public.session.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    password_hash bytea NOT NULL,
    role public.roleenum NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event ALTER COLUMN id SET DEFAULT nextval('public.event_id_seq'::regclass);


--
-- Name: session id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session ALTER COLUMN id SET DEFAULT nextval('public.session_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
464934a84d81
\.


--
-- Data for Name: attendee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attendee (user_id, event_id, session_id, created_at) FROM stdin;
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event (id, name, description, capacity, registered, status, start_at, end_at, created_by_id, created_at) FROM stdin;
1	Medical Congres Conference 2026	Annual event about AI and cloud technologies	10	0	PUBLISHED	2025-08-10 09:00:00	2025-08-10 17:00:00	1	2025-08-03 05:55:36.955596
2	AI & Cloud Conference 2025	Annual event about AI and cloud technologies	2	0	PUBLISHED	2025-08-10 09:00:00	2025-08-10 17:00:00	1	2025-08-03 16:14:57.934298
3	Integration Conference 2025	Annual event about AI and cloud technologies	5	0	PUBLISHED	2025-08-10 09:00:00	2025-08-10 17:00:00	1	2025-08-03 16:15:41.726806
\.


--
-- Data for Name: session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.session (id, event_id, title, speaker, start_at, end_at, capacity, created_at) FROM stdin;
1	1	Med conference	DR. Sofia Gomez	2025-08-01 09:00:00	2025-08-01 14:00:00	2	2025-08-03 16:16:30.157001
2	2	AI and Cloud	DR. Antal	2025-08-01 09:00:00	2025-08-01 14:00:00	2	2025-08-03 16:17:14.61547
3	3	AI and Cloud	MS David	2025-08-01 09:00:00	2025-08-01 14:00:00	5	2025-08-03 16:18:25.241659
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, email, password_hash, role, created_at) FROM stdin;
1	julian@test.com	\\x243262243132242f6b387278686630564178504d33756c42536d382f65564c2f7672374b494a51434d656865577356303354465948344444357a7565	ADMIN	2025-08-03 05:54:52.292931
2	juan@test.com	\\x243262243132246a54552e30382f3538364e516a4c4472544b33727775623743616d316b4b386e47704c4262762e34764a71613447564951714a6a79	ATTENDEE	2025-08-03 16:12:43.695535
3	sofia@test.com	\\x243262243132244b694f6f66727967654e6738434b76726c574b63657531645a5a354f72344b6872646454527975352e303570704e5a76432e4b4757	ATTENDEE	2025-08-03 16:13:05.521802
4	pedro@test.com	\\x24326224313224422f58537851506a4855367138307a69524d744c774f796f5869352e756f79504d394b585a79714c6f704e504c706c727244535453	ATTENDEE	2025-08-03 16:13:15.460964
5	juaca@test.com	\\x2432622431322431385466504d544a64315a6f70746f6b453048566a2e484f58394f4e754f3754784d44524e5a586136374e4e59304d4d587067514b	ATTENDEE	2025-08-03 16:13:26.587988
6	juana@test.com	\\x24326224313224556b75305031654749677844744945532e5052497175397039382e4842754e5a747a587a43556e524252464a534a6d354935695247	ORGANIZER	2025-08-03 16:13:44.070214
\.


--
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_id_seq', 3, true);


--
-- Name: session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.session_id_seq', 3, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: attendee attendee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee
    ADD CONSTRAINT attendee_pkey PRIMARY KEY (user_id, event_id);


--
-- Name: event event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (id);


--
-- Name: session session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_event_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_event_name ON public.event USING btree (name);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: attendee attendee_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee
    ADD CONSTRAINT attendee_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id);


--
-- Name: attendee attendee_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee
    ADD CONSTRAINT attendee_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.session(id);


--
-- Name: attendee attendee_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee
    ADD CONSTRAINT attendee_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: event event_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public."user"(id);


--
-- Name: session session_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

