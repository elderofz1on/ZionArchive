# SensorSimulator: Simulador de Dados de Sensores

## Descrição

**SensorSimulator** é um script em Python projetado para simular a geração de dados de sensores, logar esses dados em arquivos XML e enviá-los para uma fila RabbitMQ. O simulador também é capaz de gerenciar logs antigos e simular falhas nos sensores com uma probabilidade especificada.

## Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
  
## Instalação

### Pré-requisitos

- Python 3.x
- RabbitMQ

### Dependências

Instale as dependências necessárias usando pip:

```bash
pip install pika python-dotenv
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```env
RABBITMQ_URL=your_rabbitmq_url
ROUTING_KEY=your_routing_key
```

### Dados do Sensor

Configure os dados dos sensores no script conforme necessário. Exemplo:

```python
sensor_data = {
    ("M01", "S01"): (70, 100, 80),
    # ...
    ("M10", "S15"): (1500, 1900, 1765)
}
```

## Uso

### Executando o Simulador

Execute o script Python para iniciar a simulação:

```bash
python sensor_simulator.py
```

### Visualizando Logs

Os logs são salvos em arquivos XML na mesma pasta do script e são nomeados com a data correspondente.

