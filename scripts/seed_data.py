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
            {"full_name": "João Silva", "email": "joao.silva@empresa.com"},
            {"full_name": "Maria Santos", "email": "maria.santos@empresa.com"},
            {"full_name": "Pedro Oliveira", "email": "pedro.oliveira@empresa.com"},
            {"full_name": "Ana Costa", "email": "ana.costa@empresa.com"},
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
        
        # Criar credenciais RFID para cada usuário com diferentes configurações
        rfid_cards = [
            "RFID001", "RFID002", "RFID003", "RFID004", "RFID005",
            "RFID006", "RFID007", "RFID008", "RFID009", "RFID010"
        ]
        
        for i, user in enumerate(users):
            # Primeiros 3 usuários: horário comercial (08:00-18:00)
            if i < 3:
                rfid_credential = RFIDCredential(
                    user_id=user.id,
                    card_id=rfid_cards[i],
                    is_active=True,
                    has_time_restriction=True,
                    time_window_start="08:00",
                    time_window_end="18:00"
                )
                print(f"   → {user.full_name}: Horário comercial (08:00-18:00)")
            
            # Usuários 4-5: turno noturno que cruza meia-noite (22:00-06:00)
            elif i < 5:
                rfid_credential = RFIDCredential(
                    user_id=user.id,
                    card_id=rfid_cards[i],
                    is_active=True,
                    has_time_restriction=True,
                    time_window_start="22:00",
                    time_window_end="06:00"
                )
                print(f"   → {user.full_name}: Turno noturno (22:00-06:00)")
            
            # Usuários 6-7: horário integral expandido (06:00-22:00)
            elif i < 7:
                rfid_credential = RFIDCredential(
                    user_id=user.id,
                    card_id=rfid_cards[i],
                    is_active=True,
                    has_time_restriction=True,
                    time_window_start="06:00",
                    time_window_end="22:00"
                )
                print(f"   → {user.full_name}: Horário expandido (06:00-22:00)")
            
            # Usuário 8: horário de almoço restrito (12:00-14:00) - teste específico
            elif i == 7:
                rfid_credential = RFIDCredential(
                    user_id=user.id,
                    card_id=rfid_cards[i],
                    is_active=True,
                    has_time_restriction=True,
                    time_window_start="12:00",
                    time_window_end="14:00"
                )
                print(f"   → {user.full_name}: Apenas horário de almoço (12:00-14:00)")
            
            # Demais usuários: sem restrição de horário (acesso 24h)
            else:
                rfid_credential = RFIDCredential(
                    user_id=user.id,
                    card_id=rfid_cards[i],
                    is_active=True,
                    has_time_restriction=False,
                    time_window_start=None,
                    time_window_end=None
                )
                print(f"   → {user.full_name}: Sem restrição (acesso 24h)")
            
            db.add(rfid_credential)
        
        db.commit()
        print(f"✅ {len(rfid_cards)} credenciais RFID criadas")
        
        print("\n🎉 Dados iniciais populados com sucesso!")
        print("\n📋 Resumo das configurações:")
        print("   • RFID001-003: Horário comercial (08:00-18:00)")
        print("   • RFID004-005: Turno noturno (22:00-06:00)")
        print("   • RFID006-007: Horário expandido (06:00-22:00)")
        print("   • RFID008: Horário de almoço (12:00-14:00)")
        print("   • RFID009-010: Acesso 24h (sem restrição)")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
