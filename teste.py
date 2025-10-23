class Paciente_historicos:
    Texto = {}

    def Definir():
        Paciente_historicos.Texto = {"Ola": "Teste"}
        #Paciente_historicos.Testes = "Ola"    
    #def Teste():
        #print(str(Paciente_historicos.Testes))

Paciente_historicos.Definir()
print (Paciente_historicos.Texto)
#Paciente_historicos.Teste()

teste2 = Paciente_historicos()
teste2.Definir()
print (teste2.Texto)

#print (teste2.Texto)
