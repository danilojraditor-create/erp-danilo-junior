# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from datetime import date, timedelta
from typing import List, Optional
import requests
import hashlib

# =============================================================================
# 1. CONFIGURAÇÃO DO BANCO DE DADOS (SQLite Local)
# =============================================================================
DATABASE_URL = "sqlite:///erp_danilo_junior.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =============================================================================
# 2. MODELOS DO BANCO DE DADOS (ORM)
# =============================================================================
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    senha_sha256 = Column(String, nullable=False)
    nivel_permissao = Column(String, default="ADMINISTRADOR")

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome_razao = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String)
    cep = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)

class ItemEstoque(Base):
    __tablename__ = "itens_estoque"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nome_material = Column(String, nullable=False)
    quantidade_atual = Column(Float, default=0.0)
    estoque_minimo = Column(Float, default=0.0)
    preco_compra = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)

class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True, index=True)
    numero_os = Column(String, unique=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    status = Column(String, default="EM_ABERTO")  # EM_ABERTO, CONCLUIDO
    descricao_servico = Column(String)
    valor_total = Column(Float, default=0.0)

class OsMaterialConsumido(Base):
    __tablename__ = "os_materiais_consumidos"
    id = Column(Integer, primary_key=True, index=True)
    os_id = Column(Integer, ForeignKey("ordens_servico.id"))
    item_estoque_id = Column(Integer, ForeignKey("itens_estoque.id"))
    quantidade = Column(Float, nullable=False)

class FinanceiroLancamento(Base):
    __tablename__ = "financeiro_lancamentos"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # RECEITA, DESPESA
    valor = Column(Float, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    pago = Column(Boolean, default=False)

# Criar as tabelas no arquivo SQLite local
Base.metadata.create_all(bind=engine)

# =============================================================================
# 3. SCHEMAS DE VALIDAÇÃO (Pydantic)
# =============================================================================
class ClienteCreate(BaseModel):
    nome_razao: str
    cpf_cnpj: str
    telefone: str
    cep: str
    endereco: str
    bairro: str
    cidade: str
    estado: str

class LancamentoCreate(BaseModel):
    tipo: str
    valor: float
    data_vencimento: date
    pago: bool = False

# Dependência para obter a sessão do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================================================================
# 4. INSTÂNCIA DO FASTAPI E ROTAS
# =============================================================================
app = FastAPI(
    title="ERP Danilo & Junior - Serviços Elétricos",
    description="API de testes do sistema de gestão e faturamento.",
    version="1.0.0"
)

# Permitir acesso do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de inicialização para inserir dados de teste (Mock Data)
@app.on_event("startup")
def popular_banco_de_dados():
    db = SessionLocal()
    if db.query(Usuario).count() == 0:
        # Cadastra usuário padrão
        senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
        admin = Usuario(nome="Júnior Administrador", username="junior", senha_sha256=senha_hash)
        db.add(admin)
        
        # Cadastra materiais elétricos de teste
        cabo = ItemEstoque(codigo="CAB50", nome_material="Cabo Flexível SIL 10mm²", quantidade_atual=150.0, estoque_minimo=50.0, preco_compra=8.50, preco_venda=14.90)
        disjuntor = ItemEstoque(codigo="DISJ50", nome_material="Disjuntor DIN NEMA 50A", quantidade_atual=20.0, estoque_minimo=5.0, preco_compra=18.00, preco_venda=32.00)
        db.add_all([cabo, disjuntor])
        
        # Cadastra um cliente inicial
        cliente = Cliente(nome_razao="Condomínio Solar Belém", cpf_cnpj="12.345.678/0001-90", telefone="91999998888", cep="66000-000", endereco="Av. Nazaré", bairro="Nazaré", cidade="Belém", estado="PA")
        db.add(cliente)
        db.commit()
    db.close()

# --- ROTAS DE AUTENTICAÇÃO ---
@app.post("/api/auth/login", tags=["Segurança"])
def login(username: str, senha_plana: str, db: Session = Depends(get_db)):
    senha_hash = hashlib.sha256(senha_plana.encode()).hexdigest()
    user = db.query(Usuario).filter(Usuario.username == username, Usuario.senha_sha256 == senha_hash).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")
    return {"status": "Sucesso", "token_tipo": "Bearer", "usuario": user.nome}

# --- ROTAS DE CLIENTES ---
@app.get("/api/clientes/cep/{cep}", tags=["Clientes"])
def buscar_cep(cep: str):
    """Consulta o endereço automaticamente através do ViaCEP"""
    cep_limpo = cep.replace("-", "").replace(".", "")
    resposta = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/")
    if resposta.status_code != 200 or "erro" in resposta.json():
        raise HTTPException(status_code=404, detail="CEP inválido ou não encontrado.")
    dados = resposta.json()
    return {
        "endereco": dados.get("logradouro"),
        "bairro": dados.get("bairro"),
        "cidade": dados.get("localidade"),
        "estado": dados.get("uf")
    }

@app.post("/api/clientes", tags=["Clientes"])
def cadastrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@app.get("/api/clientes", tags=["Clientes"])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

# --- ROTAS DE ESTOQUE ---
@app.get("/api/estoque", tags=["Almoxarifado"])
def ver_estoque(db: Session = Depends(get_db)):
    return db.query(ItemEstoque).all()

# --- ROTAS DE ORDEM DE SERVIÇO (OS) ---
@app.post("/api/os/criar-teste", tags=["Serviços de Campo"])
def criar_os_teste(cliente_id: int, descricao: str, db: Session = Depends(get_db)):
    """Cria uma OS e vincula materiais consumidos (fios e disjuntores)"""
    nova_os = OrdemServico(
        numero_os=f"OS-2026-001",
        cliente_id=cliente_id,
        status="EM_ABERTO",
        descricao_servico=descricao,
        valor_total=250.00
    )
    db.add(nova_os)
    db.commit()
    db.refresh(nova_os)
    
    # Vincula o consumo de 15 metros do Cabo Flexível (ID 1) para esta OS
    consumo = OsMaterialConsumido(os_id=nova_os.id, item_estoque_id=1, quantidade=15.0)
    db.add(consumo)
    db.commit()
    
    return {"mensagem": "OS de teste aberta com sucesso!", "os": nova_os}

@app.post("/api/os/{os_id}/finalizar", tags=["Serviços de Campo"])
def finalizar_os(os_id: int, db: Session = Depends(get_db)):
    """Finaliza a OS, atualiza o financeiro e dá baixa automática no estoque."""
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada.")
    if os.status == "CONCLUIDO":
        return {"mensagem": "Esta OS já foi finalizada anteriormente."}
    
    # 1. Altera status da OS
    os.status = "CONCLUIDO"
    
    # 2. Dá baixa física nos materiais utilizados na OS
    materiais = db.query(OsMaterialConsumido).filter(OsMaterialConsumido.os_id == os.id).all()
    for mat in materiais:
        item = db.query(ItemEstoque).filter(ItemEstoque.id == mat.item_estoque_id).first()
        if item:
            item.quantidade_atual -= mat.quantidade # Subtrai fisicamente do estoque
            
    # 3. Lança automaticamente no Contas a Receber do Financeiro
    recebivel = FinanceiroLancamento(
        tipo="RECEITA",
        valor=os.valor_total,
        data_vencimento=date.today() + timedelta(days=5),
        pago=False
    )
    db.add(recebivel)
    db.commit()
    
    return {
        "mensagem": "OS concluída com sucesso!",
        "baixa_estoque": "Estoque deduzido!",
        "financeiro": f"Lançamento de R$ {os.valor_total} gerado no contas a receber."
    }

# --- ROTAS DO FINANCEIRO ---
@app.get("/api/financeiro/resumo", tags=["Financeiro & DRE"])
def resumo_financeiro(db: Session = Depends(get_db)):
    """Informa receitas do mês, despesas e faturamento futuro."""
    receitas = db.query(func.sum(FinanceiroLancamento.valor)).filter(FinanceiroLancamento.tipo == "RECEITA").scalar() or 0.0
    despesas = db.query(func.sum(FinanceiroLancamento.valor)).filter(FinanceiroLancamento.tipo == "DESPESA").scalar() or 0.0
    return {
        "faturamento_previsto_receber": receitas,
        "despesas_vencendo": despesas,
        "saldo_projetado": receitas - despesas
    }
