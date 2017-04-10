            if self.lastContent['nodes'] != js['nodes']:
                updater = Updater(self.authToken)
                for i in js['nodes']:
                    isNew = self.cacheContainsId(i['id'], self.lastContent)
                    if not isNew:
                        try:
                            updater.bot.sendMessage(chat_id=self.chatId,
                                                text="Neuer Knoten <a href=\"https://map.freifunk-hennef.de/#!v:m;n:{}\"\
                                                >{}</a>".format(i['id'], i['name']), parse_mode="html")
                        except KeyError:
                            logging.error(i)

            self.lastContent = js

            with open(self.filePath, "w") as file:
                json.dump(self.lastContent, file)

            logging.info("Sleeping 60s")
            sleep(60)

    def clients(self, b, u):
        """

        :type u: telegram.update.Update
        :type b: telegram.bot.Bot
        """
        req = requests.get("https://map.freifunk-hennef.de/data/metrics")

        clients = self.clientsReg.search(req.text).group(1)

        b.send_message(chat_id=u.message.chat_id,
                       text="Aktuelle Clients: *{}*".format(clients),
                       reply_to_message_id=u.message.message_id,
                       parse_mode=telegram.ParseMode.MARKDOWN)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Überprüft eine JSON-Datei nach Änderungen")
    parser.add_argument("-token", type=str, required=True, help="Authtoken für den Telegram Bot")
    parser.add_argument("-url", type=str, required=True, help="Netzwerkpfad zur JSON-Datei")
    parser.add_argument("-chat", type=int, required=True,
                        help="Telegram Chat-ID an die die Benachrichtigung gesendet werden soll")
    parsed_args = parser.parse_args()

    if not parsed_args.token:
        parser.print_help()
        exit()

    Check(parsed_args.token, parsed_args.url, parsed_args.chat).run()



