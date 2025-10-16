#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados iniciais
Evita duplicação verificando se os dados já existem
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, RFIDCredential
import uuid

def seed_data():
    """Popular dados iniciais"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem usuários
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"✅ Dados já populados: {existing_users} usuários encontrados")
            return
        
        print("🌱 Populando banco de dados com dados iniciais...")
        
        # Dados de exemplo para usuários
        users_data = [
            {"full_name": "João Silva", "email": "joao.silva@empresa.com", "has_time_restriction": False, "time_window_start": "00:00", "time_window_end": "23:59"},
            # Restrição 24h explícita (00:00 - 00:00 significa 24h na lógica do firmware)
            {"full_name": "Maria Santos", "email": "maria.santos@empresa.com", "has_time_restriction": True, "time_window_start": "00:00", "time_window_end": "00:00"}, 
            # Restrição em horário comercial
            {"full_name": "Pedro Oliveira", "email": "pedro.oliveira@empresa.com", "has_time_restriction": True, "time_window_start": "08:00", "time_window_end": "18:00"},
            # Restrição noturna (atravessa meia-noite)
            {"full_name": "Ana Costa", "email": "ana.costa@empresa.com", "has_time_restriction": True, "time_window_start": "20:00", "time_window_end": "06:00"},
            {"full_name": "Carlos Ferreira", "email": "carlos.ferreira@empresa.com"},
            {"full_name": "Lucia Rodrigues", "email": "lucia.rodrigues@empresa.com"},
            {"full_name": "Roberto Alves", "email": "roberto.alves@empresa.com"},
            {"full_name": "Fernanda Lima", "email": "fernanda.lima@empresa.com"},
            {"full_name": "Marcos Pereira", "email": "marcos.pereira@empresa.com"},
            {"full_name": "Juliana Martins", "email": "juliana.martins@empresa.com"}
        ]
        
        # Criar usuários
        users = []
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"✅ {len(users)} usuários criados")
        
        # Criar credenciais RFID para cada usuário
        rfid_cards = [
            "RFID001", "RFID002", "RFID003", "RFID004", "RFID005",
            "RFID006", "RFID007", "RFID008", "RFID009", "RFID010"
        ]
        
        for i, user in enumerate(users):
            rfid_credential = RFIDCredential(
                user_id=user.id,
                card_id=rfid_cards[i],
                is_active=True
            )
            db.add(rfid_credential)
        
        db.commit()
        print(f"✅ {len(rfid_cards)} credenciais RFID criadas")
        
        print("🎉 Dados iniciais populados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
