import abc

class ICadastro(abc.ABC):

    @abc.abstractmethod
    def salvar(self):
        pass

    @abc.abstractmethod
    def excluir(self):
        pass

    @abc.abstractmethod
    def exibir(self, id):
        pass

    @abc.abstractmethod
    def editar(self, id):
        pass

    @abc.abstractmethod
    def listar(self):
        pass