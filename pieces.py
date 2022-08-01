
import re
from tabnanny import check
from turtle import position
from typing import Set


class Piece:
    def __init__(self,name,row_number,col_number,team):
        self.row_number = row_number
        self.col_number = col_number
        self.team = team
        self.name=name
        self.check=False
        self.attacked_fields=[]
        self.king_attacks=[]#squares that need to be taken from the opponent to prevent check mate
        self.validmoves_fields=[]
        self.opponent_team='w'
        if self.team=='w':
            self.opponent_team='b'
        
    def get_row(self):
        return self.row_number
    
    def get_col(self):
        return self.col_number
    def get_coordinates(self):
        return (self.row_number,self.col_number)

    def get_team(self):
        return self.team
    
    def get_opponent_team(self):
        return self.opponent_team
    def get_name(self):
        return self.name
    

    
    def check(self,setUp):#finds out wether the piece attacks the oponents king
        attacks= self.attacks(setUp)
        for attack in attacks:
            figur=setUp.board[attack[1]][attack[0]]
            if figur!=0 and figur.get_name()=='k' and figur.get_team()==self.get_opponent_team():
                return True
        return False
    def check_prevention(self):# finds out, if check can be prevented
        return self.king_attacks
        

            
    def attacks(self,setUp):
        pass
    def get_moves(self,setUp):
        return setUp.friendly_fire_preventer(self.attacks(setUp),self.team)

    
    def change_field(self, new_row_num,new_col_num,setUp): #x
        setUp.board[self.col_number][self.row_number]=0
        self.row_number=new_row_num
        self.col_number=new_col_num
        setUp.board[new_col_num][new_row_num]=self
    
    def change_column(self, new_col_num): #y
        self.col_number=new_col_num
    


      

class Pawn(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
        
    
    def attacks(self, setUp):
        self.attacked_fields.extend(setUp.pawn_attacks(self.get_col(),self.get_row(),self.get_team()))
        return self.attacked_fields
    
    def check_prevention(self,setUp):
        if self.check(setUp):
            return self.get_coordinates()

    
    def get_moves (self, setUp):
     self.validmoves_fields.extend(setUp.pawn_moves(self.get_attacks(),self.get_col(),self.get_row(),self.get_team()))
     return self.validmoves_fields

class Knight(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
    def attacks(self, setUp):
        self.attacked_fields.extend(setUp.horse_moves(self.get_col(),self.get_row()))
        return self.attacked_fields
    def check_prevention(self,setUp):
        if self.check(setUp):
            return self.get_coordinates()
        
        
        

class Bishop(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)

    def attacks(self,setUp):
        diagonal1=(setUp.diagonal1(self.get_col(),self.get_row()))
        diagonal2=(setUp.diagonal2(self.get_col(),self.get_row()))
        self.attacked_fields = diagonal1[0]+diagonal2[0]
        self.king_attacks=diagonal1[1]+diagonal2[1]
        return self.attacked_fields
        
class Rook(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
    def attacks(self, setUp):
        horizontal = (setUp.horizontal_moves(self.get_col(),self.get_row()))
        vertical = (setUp.vertical_moves(self.get_col(),self.get_row()))
        self.attacked_fields=horizontal[0]+vertical[0]
        self.king_attacks=horizontal[1]+vertical[1]
        return self.attacked_fields


    # def attacks(self):
    #     if self.team=='w':
class Queen(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
    def attacks(self,setUp):
        horizontal = (setUp.horizontal_moves(self.get_col(),self.get_row()))
        vertical = (setUp.vertical_moves(self.get_col(),self.get_row()))
        self.attacked_fields=horizontal[0]+vertical[0]
        self.king_attacks=horizontal[1]+vertical[1]
        diagonal1=(setUp.diagonal1(self.get_col(),self.get_row()))
        diagonal2=(setUp.diagonal2(self.get_col(),self.get_row()))
        self.attacked_fields = diagonal1[0]+diagonal2[0]
        self.king_attacks=diagonal1[1]+diagonal2[1]

        return self.attacked_fields     

class King(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
        
    def can_move(self,setUp):
        if self.get_moves (setUp):
            return True
        return False
    
    def attacks(self, setUp):
        return setUp.king_attacks(self.get_col(),self.get_row())
    
    def get_moves (self, setUp):
        position=(self.get_row(),self.get_row())
        
        attacks=self.attacks(setUp)
        opponent_attacks=setUp.get_all_attacks(self.get_opponent_team())
        for attack in attacks:
            if attack in opponent_attacks[:]:
                attacks.remove(attack)
        for attack in attacks[:]:
            self.change_field(attack[0],attack[1],setUp)
            opponent_attacks=setUp.get_all_attacks(self.get_opponent_team())
            if attack in opponent_attacks:
                attacks.remove(attack)
        self.change_field(position[0],position[1],setUp)
        return attacks


        

        




        


