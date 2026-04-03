-- ========================================
-- PROCEDURES FOR PHONEBOOK
-- ========================================

-- 1. Procedure: add or update a single contact
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;

-- 2. Procedure: delete contact by name/surname or phone
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_surname VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE (p_name IS NOT NULL AND name = p_name)
       OR (p_surname IS NOT NULL AND surname = p_surname)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;

-- 3. Procedure: bulk insert contacts from array
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[],
    p_surnames VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN array_lower(p_names,1)..array_upper(p_names,1) LOOP
        -- проверяем корректность телефона
        IF p_phones[i] ~ '^[0-9\s\+\-]+$' THEN
            CALL upsert_contact(p_names[i], p_surnames[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %', p_phones[i];
        END IF;
    END LOOP;
END;
$$;