

-- 1. ТАБЛИЦА КОНТАКТОВ

-- Главная таблица, от которой всё строится

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,              -- уникальный ID контакта (автоувеличение)
    name VARCHAR(100) NOT NULL          -- имя контакта (обязательное поле)
);


-- 2. ТАБЛИЦА ГРУПП



CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,              -- уникальный ID группы
    name VARCHAR(50) UNIQUE NOT NULL    -- название группы (уникальное)
);


-- 3. ДОПОЛНЕНИЕ ТАБЛИЦЫ CONTACTS

-- Добавляем новые поля к контактам

ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),  -- email адрес
    ADD COLUMN IF NOT EXISTS birthday DATE,       -- дата рождения
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id), -- связь с группой
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP; 
    -- дата создания контакта (ставится автоматически)


-- 4. ТАБЛИЦА ТЕЛЕФОНОВ

-- Один контакт может иметь много телефонов

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY, 
    -- уникальный ID телефона

    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    -- внешний ключ:


    phone VARCHAR(20) NOT NULL,
    -- номер телефона

    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
    -- тип телефона (ограниченные значения)
);