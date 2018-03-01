# Air quality monitor for your city

## Example

[![Telegram Chat](https://img.shields.io/badge/Telegram_Channel-BeijingAir-blue.svg)](https://t.me/BeijingAir)

## Getting Started

### Prerequisites

Obtain `aqicn_token` by requesting Air Quality API [here](http://aqicn.org/data-platform/token/#/).

Obtain your `city` id by running the GET request below
```
https://api.waqi.info/search/?keyword={your_city_name}&token={your_token}
```
For example, we got `@3303` for Beijing.

Create a Telegram Bot, instructions can be found [here](https://core.telegram.org/bots).

send a message to the bot you just created, run the following request to get your telegram_id
`https://api.telegram.org/bot<BOTID>/getUpdates`

Fill the `tester_id` field with your telegram_id.

Create a Telegram Channel for publishing real-time data.

For obtaining `channel_id`, check [here](https://stackoverflow.com/questions/33858927/how-to-obtain-the-chat-id-of-a-private-telegram-channel).
### Installation

```
git clone git@github.com:Eth4nZ/aqi-monitor.git && cd aqi-monitor

pip3 install -r requirements.txt

cp sample_config.json config.json
```
complete `config.json` with the tokens you got in the previous section.

### Usage

```
python3 beijing_air_monitor.py
```
#### Debug
`"debug_mode": "true"`
Message will be sent to your private account with 5 minutes interval

#### Production
`"debug_mode": "false"`
Message will be sent to telegram channel with 60 minutes interval


