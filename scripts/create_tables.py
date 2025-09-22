#!/usr/bin/env python3
"""
Script para criar tabelas no banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import User, RFIDCredential, AccessLog, ErrorLog

def create_tables():
    """Criar todas as tabelas"""
    print("🔧 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_tables()
