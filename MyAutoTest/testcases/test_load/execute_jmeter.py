import os

"""
通过os.system 发送 cmd 命令，命令行启动 jmeter
"""

if __name__ == "__main__":
    os.chdir("C:\\Users\\Zhou\\apache-jmeter-5.6.2\\apache-jmeter-5.6.2\\bin")
    print(os.getcwd())
    os.system(
        r"jmeter -n -t C:\Users\EDY\Desktop\layout.jmx -l C:\Users\Zhou\apache-jmeter-5.6.2\results.html -e -o C:\Users\Zhou\apache-jmeter-5.6.2\result")
