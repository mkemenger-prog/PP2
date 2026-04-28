-- Процедура для добавления нового телефона контакту
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,   -- имя контакта
    p_phone VARCHAR,          -- номер телефона
    p_type VARCHAR            -- тип (home/work/mobile)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;     -- переменная для хранения ID контакта
BEGIN
    -- ищем контакт по имени
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    -- если контакт не найден → ошибка
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Контакт не найден';
    END IF;

    -- добавляем телефон в таблицу phones
    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- Процедура для перемещения контакта в группу
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,   -- имя контакта
    p_group_name VARCHAR      -- название группы
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;       -- ID группы
BEGIN
    -- создаём группу, если она ещё не существует
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    -- получаем ID группы
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    -- обновляем контакт (назначаем новую группу)
    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;


-- Функция поиска по имени, email и телефону
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    -- LEFT JOIN: показываем контакт даже если у него нет телефона

    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
    -- поиск по всем полям (без учёта регистра)
END;
$$;