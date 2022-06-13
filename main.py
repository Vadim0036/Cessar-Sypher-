import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


class CessarSypher:

    def __init__( self ):

        self.main_window = tkinter.Tk()
        self.main_window.title('Cessar Sypher')
        self.main_window.iconbitmap('/Users/vadim/Documents/Programming/Python/Programs/Cessar Sypher/Pictures/025_-_Private_Password-lock-cryptography-encrypt-512.webp')

        self.firstPageFrame = tkinter.Frame( self.main_window )
        self.firstPage = FirstPage( self.firstPageFrame )
        self.firstPage.setLinkCSFP(self)

        self.fileEncFrame = tkinter.Frame( self.main_window )
        self.fileEncPage = FileEncPage( self.fileEncFrame )

        self.textEncFrame = tkinter.Frame( self.main_window )
        self.textEncPage = TextEncPage( self.textEncFrame )



    def start( self ):
        self.firstPageFrame.pack()
        self.main_window.mainloop()

    def switchToFilePage( self ):

        self.firstPageFrame.pack_forget()
        self.fileEncFrame.pack()

    def switchToTextPage( self ):

        self.firstPageFrame.pack_forget()
        self.textEncFrame.pack()

    def quit( self ):

        self.main_window.destroy()


 
class FirstPage:

    def __init__( self, frame ):
        
        self.mainLabel = self.createLabels( frame )


        self.enscryptFileButton = self.createButtons( frame, 1, 0, 'Enscrypt\ntxt file', self.enscryptTxtFileCommand )
        self.enscryptTextButton = self.createButtons( frame, 1, 1, 'Type text\nto enscrypt', self.enscryptTextCommand )
        


    def createLabels( self, frame ):

        label = tkinter.Label( frame )
        label.grid( row=0, column=0, sticky='NEWS', columnspan=2 )
        label.config( text= 'Enscryption Program', font=('Comic Sans MS', 30), height=2 )
        return label

    def createButtons( self, frame,  r, c, text, command  ):
        button = tkinter.Button( frame )
        button.grid( row=r, column=c, sticky='NEWS', padx=8, pady=8 )
        button.config( text=text, font=('Comic Sans MS', 19), height=2, width=15 )
        button.config( command= command )
        return button

    def enscryptTxtFileCommand( self ):

        self.linkCSFP.switchToFilePage()

    def enscryptTextCommand( self ):

        self.linkCSFP.switchToTextPage()

    def setLinkCSFP( self, link ):

        self.linkCSFP = link


class File:

    def __init__( self ):

        self.file = self.getFile()
        self.lines = []


    def getFile( self ):

        file = filedialog.askopenfilename()
        return file

    def getLines( self ):

        with open( self.file, 'r' ) as f: 
            
            for line in f:
                self.lines.append(line.strip())

        return( self.lines )


class FileEncPage:

    def __init__( self, frame ):

        self.chooseFileLabel = self.createLabels( frame, 0, 0, 'Choose file: ', None )
        self.keyLabel = self.createLabels( frame, 1, 0, 'Key: ', None )

        self.fileSearchButton = self.createButtons( frame, 0, 1, 'Click To Get File', self.getText, 2 )
    
        encryptCommand = lambda: self.encrypt( int(self.keyEntry.get()) )
        decryptCommand = lambda: self.decrypt( int(self.keyEntry.get()) )

        self.enscryptButton = self.createButtons( frame, 2, 0, 'ENCRYPT', encryptCommand, 12 )
        self.decryptButton = self.createButtons( frame, 2, 1, 'DECRYPT', decryptCommand, 12 )

        self.keyEntry = self.createEntry( frame, 1, 1)


    def createLabels( self, frame, r, c , text, cp ):
        
        label = tkinter.Label(frame)
        label.grid( row=r, column=c, sticky='NEWS', columnspan=cp )
        label.config( text= text, font=( 'Comic Sans MS', 20 ), height=2, width=10 )
        return label

    def createButtons( self, frame, r, c, text, command, w ):

        button = tkinter.Button( frame )
        button.grid( row=r, column=c, sticky='NEWS', pady= 12 )
        button.config( text=text, font=('Comic Sans MS', 20), height=2, width=w )
        button.config( command= command )
        return button

    def createEntry( self, frame, r, c ):

        entry = tkinter.Entry( frame )
        entry.grid( row=r, column=c, sticky='NEWS' )
        entry.config(width=5, font=('Comic Sans MS', 20))
        return entry 

    def getText( self ):

        file_obj = File()
        file = file_obj.file

        with open(file, 'r') as f: 

            text = f.read()

            self.lines = text.splitlines()

    def encrypt( self, key ):
        
        digAlpha = "0123456789"
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        symbols = "!@#$%^&*()-_=+\|][{>}:;,.<""''?/`~"
        encryptedLine = ''
        encryptedText = ''


        spot = 0 
        

        while spot <= len(self.lines)-1:
        
            line = self.lines[spot]
            
            spot += 1

            spot2 = 0
            encryptedLine = ''

            while spot2 <= len(line)-1:

                cher = line[spot2]
                
                if self.checkNum( cher ):
                    
                    encryptedIndex = self.getIndex( cher ) + key
                    
                    while encryptedIndex >= len(digAlpha) -1:
                        encryptedIndex -= 10

                    encryptedCher = digAlpha[encryptedIndex]

                elif self.check( cher ):
            
                    encryptedCher = ' '

                elif self.checkSymbols( cher ):

                    encryptedIndex = self.getSymbolIndex( cher ) + key

                    while encryptedIndex >= len(symbols)-1:
                        encryptedIndex -= 32

                    encryptedCher = symbols[encryptedIndex]

                else:

                    encryptedIndex = self.getCherIndex( cher ) + key

                    while encryptedIndex >= len(alpha)-1:
                        encryptedIndex -= 26 

                    encryptedCher = alpha[encryptedIndex]
                
                encryptedLine = encryptedLine + encryptedCher
                spot2 += 1
            
            encryptedText = encryptedText + encryptedLine + '\n'


        self.createEncryptedFile( encryptedText )

        messagebox.showinfo(message='The file with encrypted text has been created ')

    
    def decrypt( self, key ):
        
        digAlpha = "0123456789"
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        symbols = "!@#$%^&*()-_=+\|][{>}:;,.<""''?/`~"
        decryptedLine = ''
        decryptedText = ''


        spot = 0 
        

        while spot <= len(self.lines)-1:
        
            line = self.lines[spot]
            
            spot += 1

            spot2 = 0
            decryptedLine = ''

            while spot2 <= len(line)-1:

                cher = line[spot2]
                
                if self.checkNum( cher ):
                    
                    decryptedIndex = self.getIndex( cher ) + key
                    
                    while decryptedIndex < 0:
                        decryptedIndex += 10

                    decryptedCher = digAlpha[decryptedIndex]

                elif self.check( cher ):
            
                    decryptedCher = ' '

                elif self.checkSymbols( cher ):

                    decryptedIndex = self.getSymbolIndex( cher ) - key

                    while decryptedIndex < 0:
                        decryptedIndex += 32

                    decryptedCher = symbols[decryptedIndex]

                else:

                    decryptedIndex = self.getCherIndex( cher ) - key

                    while decryptedIndex < 0:
                        decryptedIndex += 26 

                    decryptedCher = alpha[decryptedIndex]
                
                decryptedLine = decryptedLine + decryptedCher
                spot2 += 1
            
            decryptedText = decryptedText + decryptedLine + '\n'


        self.createDecryptedFile( decryptedText )
        
        messagebox.showinfo(message='The file with decrypted text has been created ')
        

    def checkNum( self, cher ):
        digAlpha = "0123456789"
        
        for spot in range(len(digAlpha)):
            numCher = digAlpha[spot]

            if cher == numCher:
                return True

        return False

    def check( self, cher ):
        newCher = cher.strip()

        if newCher == "":
            return True
            
        else:
            return False
    
    def checkSymbols( self, cher ):
        newCher = cher.strip()
        symbols = "!@#$%^&*()-_=+\|][{>}:;.,<""''?/`~"
        for spot in range(len(symbols)):
            symCher = symbols[spot]
            if newCher == symCher: 
                return True          
        return False

    def getIndex( self, cher ):
        newCher = cher.strip()
        digAlpha = "0123456789"
        cherIndex = digAlpha.index(newCher)
        return cherIndex

    def getCherIndex( self, cher ):
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cher = cher.upper()
        cherIndex = alpha.index( cher )
        return cherIndex

    def getSymbolIndex( self, cher ):
        newCher = cher.strip()
        symbols = "!@#$%^&*()-_=+\|][{>}:;.,<""''?/`~"
        symIndex = symbols.index(newCher)
        return symIndex
    
    def createEncryptedFile( self, text ):

        with open('encryptedText1', 'w') as ef:
            ef.write(text)

    def createDecryptedFile( self, text ):

        with open('decryptedText', 'w') as df:
            df.write(text)


class TextEncPage:

    def __init__( self, frame ):

        self.main_label = self.createLabels( frame, 0, 0, 'Encryption program', 2, 35 )
        self.entryWordLabel = self.createLabels( frame, 1, 0, 'Enter text: ', None, 28 )
        self.enterKeyLabel = self.createLabels( frame, 2, 0, 'Enter key: ', None, 28 ) 
        self.finalText = self.createLabels( frame, 4, 0, 'Final Text: ', None, 30)


        self.textEntry = self.createEntries( frame, 1, 1 )
        self.keyEntry = self.createEntries( frame, 2, 1 )

        commandEncrypt = lambda: self.encrypt( int(self.keyEntry.get()) , self.textEntry.get() )
        commandDecrypt = lambda: self.decrypt( int(self.keyEntry.get()) , self.textEntry.get() )


        self.encryptButton = self.createButtons( frame, 3, 0, 'ENCRYPT', commandEncrypt )
        self.decryptButton = self.createButtons( frame, 3, 1, 'DECRYPT', commandDecrypt )



    def createLabels( self, frame, r, c, text, cp, fontSize ):

        label = tkinter.Label( frame )
        label.grid( row=r, column=c, sticky='NEWS', columnspan=cp, pady=10 )
        label.config( text=text, font=('Comic Sans MS', fontSize) )
        return label

    def createButtons( self, frame, r, c, text, command ):

        button = tkinter.Button( frame )
        button.grid( row=r, column=c, sticky='NEWS', padx=10, pady=10 )
        button.config( text=text, font=('Comic Sans MS', 28), width=10, height=2)
        button.config( command=command )
        return button 

    def createEntries( self, frame, r, c ):

        entry = tkinter.Entry( frame )
        entry.grid( row=r, column=c, sticky='NEWS')
        entry.config( font=('Comic Sans MS',28 ), width=18)
        return entry

    
    def encrypt( self, key, text ):

        digAlpha = "0123456789"
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        symbols = "!@#$%^&*()-_=+\|][{>}:;,.<""''?/`~"
        encryptedText = ''
        encryptedCher = ''

        spot = 0
        
        while spot <= len(text)-1:

            cher = text[spot]

            if self.checkNum( cher ):
                
                encryptedIndex = self.getIndex( cher ) + key
                while encryptedIndex >= len(digAlpha) -1:
                    encryptedIndex -= 10
                    
                encryptedCher = digAlpha[encryptedIndex]

            elif self.check( cher ):

                encryptedCher = ' '

            elif self.checkSymbols( cher ):

                encryptedIndex = self.getSymbolIndex( cher ) + key
                while encryptedIndex >= len(symbols)-1:
                    encryptedIndex -= 32

                encryptedCher = symbols[encryptedIndex]

            else:

                encryptedIndex = self.getCherIndex( cher ) + key
                while encryptedIndex >= len(alpha)-1:
                    encryptedIndex -= 26
                
                encryptedCher = alpha[encryptedIndex]


            encryptedText = encryptedText + encryptedCher

            spot += 1

        self.showFinalText( f'Encrypted Text: {encryptedText}' )


    def decrypt( self, key, text ):

        digAlpha = "0123456789"
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        symbols = "!@#$%^&*()-_=+\|][{>}:;,.<""''?/`~"
        decryptedText = ''
        decryptedCher = ''

        spot = 0
        while spot <= len(text)-1:

            cher = text[spot]

            if self.checkNum( cher ):
                
                decryptedIndex = self.getIndex( cher ) - key
                while decryptedIndex < 0:
                    decryptedIndex += 10

                decryptedCher = digAlpha[decryptedIndex]
                
            elif self.check( cher ):

                decryptedCher = ' '

            elif self.checkSymbols( cher ):

                decryptedIndex = self.getSymbolIndex( cher ) - key
                while decryptedIndex < 0:
                    decryptedIndex += 32

                decryptedCher = symbols[decryptedIndex]

            else:

                decryptedIndex = self.getCherIndex( cher ) - key
                while decryptedIndex < 0: 
                    decryptedIndex += 26
                
                decryptedCher = alpha[decryptedIndex]
            
            decryptedText = decryptedText + decryptedCher

            spot +=1 

        self.showFinalText( f'Decrypted Text: {decryptedText}' )


    def showFinalText( self, text ):

        self.finalText.config(text= text)

    def checkNum( self, cher ):
        digAlpha = "0123456789"
        
        for spot in range(len(digAlpha)):
            numCher = digAlpha[spot]

            if cher == numCher:
                return True

        return False

    def check( self, cher ):

        if cher == " ":
            return True

    
    def checkSymbols( self, cher ):
        newCher = cher.strip()
        symbols = "!@#$%^&*()-_=+\|][{>}:;.,<""''?/`~"
        for spot in range(len(symbols)):
            symCher = symbols[spot]
            if newCher == symCher: 
                return True          
        return False

    def getIndex( self, cher ):
        newCher = cher.strip()
        digAlpha = "0123456789"
        cherIndex = digAlpha.index(newCher)
        return cherIndex

    def getCherIndex( self, cher ):
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cher = cher.upper()
        cherIndex = alpha.index( cher )
        return cherIndex

    def getSymbolIndex( self, cher ):
        newCher = cher.strip()
        symbols = "!@#$%^&*()-_=+\|][{>}:;.,<""''?/`~"
        symIndex = symbols.index(newCher)
        return symIndex

        

enscrypt = CessarSypher()
enscrypt.start()