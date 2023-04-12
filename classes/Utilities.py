class Text():
    def Green(text):
        return "\033[32m"+text+"\033[0m "

    def Red(text):
        return "\033[31m"+text+"\033[0m "

    def Yellow(text):
        return "\033[33m"+text+"\033[0m "
    
    def Purple(text):
        return "\033[35m"+text+"\033[0m "

    def Underline(text):
        return "\033[4m"+text+"\033[0m "