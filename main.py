import telebot
import yaml
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', type=str, default='./config.yaml',
                        help='Path to the file, where base configuration is being stored.')
    parser.add_argument('--api-key', type=str, required=True,
                        help='API-key of your bot.')
    
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    bot = telebot.TeleBot(args.api_key)

    with open(args.config_path) as config:
        config = yaml.safe_load(config)

    print(config)