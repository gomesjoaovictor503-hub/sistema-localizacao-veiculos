from django.db import models

# Esta classe representa a tabela de carros no seu banco de dados
class Carro(models.Model):
    # Definimos as opções de status para as abas do seu sistema
    STATUS_CHOICES = [
        ('pre_localizado', 'Pré-localizado'),
        ('localizado', 'Localizado'),
        ('apreendido', 'Apreendido'),
    ]

    # --- NOVO CAMPO ABAIXO ---
    # Este campo guardará o nome/apelido que o usuário digitou para acessar
    usuario_acesso = models.CharField(
        max_length=100, 
        default='admin', 
        verbose_name="Nome de Acesso"
    )
    # -------------------------

    # Campos do cadastro
    placa = models.CharField(max_length=7, unique=True, verbose_name="Placa do Veículo")
    cor = models.CharField(max_length=30, verbose_name="Cor")
    escritorio = models.CharField(max_length=100, verbose_name="Escritório Responsável")

    # Este campo 'status' é o que vai separar os carros nas abas
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pre_localizado',
        verbose_name="Situação atual"
    )

    # Registra automaticamente a data e hora que o carro foi cadastrado
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    # Isso faz com que, ao listar os carros, apareça a placa no painel
    def __str__(self):
        return f"{self.placa} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
        ordering = ['-data_criacao']  # Mostra os mais novos primeiro
