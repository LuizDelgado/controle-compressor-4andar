import paho.mqtt.client as mqtt  # Importa a biblioteca MQTT para interação com o protocolo MQTT.
from dotenv import load_dotenv  # Importa a função para carregar variáveis de ambiente de um arquivo .env.
import os  # Importa o módulo os para interação com o sistema operacional, como ler variáveis de ambiente.
import time  # Importa o módulo time para usar delays (pausas).

# Carrega as variáveis de ambiente da aplicação
load_dotenv()

class MQTTClient:
    # Construtor da classe, inicializa uma instância da classe com as configurações necessárias.
    def __init__(self, broker, port, username, password, client_id):
        self.broker = broker  # Endereço do broker MQTT.
        self.port = port  # Porta para a conexão com o broker.
        self.username = username  # Nome de usuário para autenticação no broker.
        self.password = password  # Senha para autenticação no broker.
        self.client_id = client_id  # ID do cliente para identificação no broker.
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=self.client_id)  # Cria o objeto cliente MQTT com a versão de callback especificada.
        self.configure_client()  # Chama o método para configurar o cliente MQTT.

    # Método para configurar o cliente MQTT, definindo credenciais e handlers (funções de callback).
    def configure_client(self):
        self.client.username_pw_set(self.username, self.password)  # Configura o nome de usuário e senha no cliente MQTT.
        self.client.on_connect = self.on_connect  # Define o handler para o evento de conexão.
        self.client.on_disconnect = self.on_disconnect  # Define o handler para o evento de desconexão.

    # Função chamada quando o cliente se conecta ao broker.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT.")  # Sucesso na conexão.
        else:
            print(f"Falha na conexão com o servidor, código de retorno: {rc}")  # Falha na conexão.

    # Função chamada quando o cliente se desconecta do broker.
    def on_disconnect(self, client, userdata, rc):
        print("Desconectado do broker MQTT.")  # Informa sobre a desconexão.

    # Método para publicar uma mensagem em um tópico específico.
    def publish(self, topic, message):
        try:
            self.client.connect(self.broker, self.port)  # Conecta ao broker MQTT.
            self.client.loop_start()  # Inicia o loop em segundo plano para processar callbacks de rede.
            self.client.publish(topic, message)  # Publica a mensagem no tópico especificado.
            #Delay necessário para evitar perda de envio de mensagem devido a QoS 
            time.sleep(2)  # Espera 2 segundos para garantir a entrega da mensagem.
        finally:
            self.client.loop_stop()  # Para o loop de rede.
            self.client.disconnect()  # Desconecta do broker MQTT.


