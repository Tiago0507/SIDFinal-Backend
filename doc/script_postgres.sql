-- Insertar Compañías (Clientes empresariales reales)
INSERT INTO company (nit, name, industry, address, phone, email, country, state) VALUES 
('900456123', 'TechForce Solutions', 'Technology', 'Calle 100 #15-45, Bogotá', '601-4567890', 'contact@techforce.co', 'Colombia', 'Bogotá'),
('901234567', 'MediCare Plus', 'Healthcare', 'Carrera 80 #35-21, Medellín', '604-3456789', 'info@medicare.com.co', 'Colombia', 'Antioquia'),
('800789123', 'BankFinance Corp', 'Banking', 'Calle 72 #7-64, Bogotá', '601-2345678', 'contact@bankfinance.com.co', 'Colombia', 'Bogotá'),
('805555111', 'EduTech Colombia', 'Education', 'Calle 5 #38-25, Cali', '602-8901234', 'info@edutech.edu.co', 'Colombia', 'Valle');

-- Insertar Contactos
INSERT INTO contact (contact_id, nit, first_name, last_name, position, phone, email, last_interaction_date) VALUES 
('C001', '900456123', 'Juan', 'Pérez', 'IT Director', '315-1234567', 'juan.perez@techforce.co', '2024-01-15'),
('C002', '901234567', 'María', 'González', 'CTO', '316-7654321', 'maria.gonzalez@medicare.com.co', '2024-01-20'),
('C003', '800789123', 'Carlos', 'Rodríguez', 'Infrastructure Manager', '317-8901234', 'carlos.rodriguez@bankfinance.com.co', '2024-01-18'),
('C004', '805555111', 'Ana', 'Martínez', 'Technology Director', '318-5678901', 'ana.martinez@edutech.edu.co', '2024-01-22');

-- Insertar Departamentos
INSERT INTO department (department_id, department_name, description) VALUES 
('D001', 'IT', 'Tecnología de la Información'),
('D002', 'Infrastructure', 'Infraestructura Tecnológica'),
('D003', 'Security', 'Seguridad Informática'),
('D004', 'Digital Innovation', 'Innovación Digital');

-- Relacionar Contactos con Departamentos
INSERT INTO contact_department (contact_id, department_id, assignment_date) VALUES 
('C001', 'D001', '2024-01-01'),
('C002', 'D002', '2024-01-01'),
('C003', 'D003', '2024-01-01'),
('C004', 'D004', '2024-01-01');

-- Insertar Categorías de Equipos
INSERT INTO category (category_id, category_name, description) VALUES 
('CAT001', 'Laptops', 'Computadores portátiles empresariales'),
('CAT002', 'Desktop PCs', 'Computadores de escritorio'),
('CAT003', 'Servers', 'Servidores empresariales'),
('CAT004', 'Networking', 'Equipos de red'),
('CAT005', 'Mobile Devices', 'Dispositivos móviles empresariales');

-- Insertar Contratos
INSERT INTO contract (contract_id, nit, contract_number, start_date, end_date, monthly_value) VALUES 
('CTR001', '900456123', 'TECH-2024-001', '2024-01-01', '2025-01-01', 5000000.00),
('CTR002', '901234567', 'MED-2024-001', '2024-01-15', '2025-01-15', 3500000.00),
('CTR003', '800789123', 'BANK-2024-001', '2024-02-01', '2025-02-01', 7500000.00),
('CTR004', '805555111', 'EDU-2024-001', '2024-01-20', '2025-01-20', 4500000.00);

-- Insertar Certificados de Entrega
INSERT INTO delivery_certificate (certificate_id, contract_id, delivery_date, notes) VALUES 
('DC001', 'CTR001', '2024-01-05', 'Entrega inicial equipos TechForce'),
('DC002', 'CTR002', '2024-01-20', 'Entrega inicial equipos MediCare'),
('DC003', 'CTR003', '2024-02-05', 'Entrega inicial equipos BankFinance'),
('DC004', 'CTR004', '2024-01-25', 'Entrega inicial equipos EduTech');

-- Insertar Equipos
INSERT INTO equipment (equipment_id, certificate_id, inventory_code, description, active, category_id) VALUES 
('EQ001', 'DC001', 'LT-2024-001', 'ThinkPad X1 Carbon Gen 10', true, 'CAT001'),
('EQ002', 'DC001', 'LT-2024-002', 'Dell Latitude 7430', true, 'CAT001'),
('EQ003', 'DC002', 'DT-2024-001', 'HP EliteDesk 800 G8', true, 'CAT002'),
('EQ004', 'DC002', 'SV-2024-001', 'Dell PowerEdge R750', true, 'CAT003'),
('EQ005', 'DC003', 'NW-2024-001', 'Cisco Catalyst 9200', true, 'CAT004'),
('EQ006', 'DC004', 'MB-2024-001', 'iPad Pro 12.9 2024', true, 'CAT005');

-- Insertar Roles
INSERT INTO role (role_id, role_name, description) VALUES 
('R001', 'Admin', 'Administrador del sistema'),
('R002', 'User', 'Usuario regular'),
('R003', 'Manager', 'Gerente de cuenta');

-- Insertar Cuentas de Usuario (password_hash sería realmente un hash, aquí es ejemplo)
INSERT INTO user_account (user_id, nit, username, password_hash, email) VALUES 
('U001', '900456123', 'juan.perez', '$2b$12$vRPQAh3cGgCHscy6MXOUO./zCSMJbvlg36rf98EEG7u/72bxtNg96', 'juan.perez@techforce.co'), --password: hash1234
('U002', '901234567', 'maria.gonzalez', '$2b$12$ULTgjsjBD2Dpb63LlBSl8e/ZxXnGNaDMXW8i.WqFc.Z7HArBydOg.', 'maria.gonzalez@medicare.com.co'), --password: hash12345
('U003', '800789123', 'carlos.rodriguez', '$2b$12$sN7bKZ.4vX00fPmywl6T0udggkWDXeN3BiQdwl9fJ3yBkGemZ20.m', 'carlos.rodriguez@bankfinance.com.co'), --password: hash123456
('U004', '805555111', 'ana.martinez', '$2b$12$PHJCMmaNKwWMNWaDPbDOIOZFR8Om8zmgkF8IJb4yQLmejIcZrM2Iq', 'ana.martinez@edutech.edu.co'); --password: hash1234567

-- Asignar Roles a Usuarios
INSERT INTO user_role (user_id, role_id) VALUES 
('U001', 'R001'),
('U002', 'R002'),
('U003', 'R002'),
('U004', 'R003');

-- Insertar oportunidades
INSERT INTO opportunity (opportunity_id, nit, contact_id, opportunity_name, description, estimated_value, estimated_close_date, status, success_probability) VALUES 
('OPP001', '900456123', 'C001', 'Actualización Infraestructura', 'Renovación completa de equipos', 150000000.00, '2024-06-30', 'open', 75.00),
('OPP002', '901234567', 'C002', 'Proyecto Móvil', 'Dotación tablets área médica', 80000000.00, '2024-05-15', 'negotiation', 60.00);

-- Insertar etapas de oportunidad
INSERT INTO opportunity_stage (stage_id, stage_name, description) VALUES 
('ST001', 'Initial Contact', 'Primer contacto con el cliente'),
('ST002', 'Proposal', 'Propuesta enviada'),
('ST003', 'Negotiation', 'En negociación'),
('ST004', 'Closed Won', 'Oportunidad ganada');

-- Historial de etapas
INSERT INTO opportunity_stage_history (opportunity_id, stage_id, change_date, notes) VALUES 
('OPP001', 'ST001', '2024-01-10', 'Inicio del proceso'),
('OPP001', 'ST002', '2024-01-20', 'Propuesta enviada'),
('OPP002', 'ST001', '2024-01-15', 'Inicio del proceso');

-- Productos/Servicios
INSERT INTO product_service (product_service_id, product_service_name, description, price) VALUES 
('PS001', 'Renting Laptops Premium', 'Servicio de renting laptops alta gama', 250000.00),
('PS002', 'Renting Servidores', 'Servicio de renting servidores empresariales', 500000.00),
('PS003', 'Soporte TI', 'Servicio de soporte técnico', 100000.00);

-- Relacionar Oportunidades con Productos
INSERT INTO opportunity_product_service (opportunity_id, product_service_id, quantity, negotiated_price) VALUES 
('OPP001', 'PS001', 20, 200000.00),
('OPP001', 'PS003', 1, 90000.00),
('OPP002', 'PS001', 10, 225000.00);