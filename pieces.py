from attr import attr


class Piece:
    def __init__(self,name,row_number,col_number,team):
        self.row_number = row_number
        self.col_number = col_number
        self.team = team
        self.name=name
        self.attacked_fields=[]
        self.validmoves_fields=[]
        
    def get_row(self):
        return self.row_number
    
    def get_col(self):
        return self.col_number

    def get_team(self):
        return self.team
    

    def attacks(self,setUp):
        pass
    def valid_moves(self,setUp):
        return setUp.friendly_fire_preventer(self.attacked_fields,self.team)

    
    def change_row(self, new_row_num): #x
        self.row_number=new_row_num
    
    def change_column(self, new_col_num): #y
        self.col_number=new_col_num
    

      

class Pawn(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)

class Knight(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
    def attacks(self, setUp):
        self.attacked_fields.extend(setUp.horse_moves(self.get_col(),self.get_row(),self.get_team()))
        return self.attacked_fields
        
        
        

class Bishop(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)

    def attacks(self,setUp):
        self.attacked_fields.extend(setUp.diagonal1(self.get_col(),self.get_row()))
        self.attacked_fields.extend(setUp.diagonal2(self.get_col(),self.get_row()))
        return self.attacked_fields
        
class Rook(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
    def attacks(self, setUp):
        self.attacked_fields.extend(setUp.horizontal_moves(self.get_col(),self.get_row()))
        self.attacked_fields.extend(setUp.vertical_moves(self.get_col(),self.get_row()))
        return self.attacked_fields


    # def attacks(self):
    #     if self.team=='w':
class Queen(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)
    def attacks(self,setUp):
        self.attacked_fields.extend(setUp.diagonal1(self.get_col(),self.get_row()))
        self.attacked_fields.extend(setUp.diagonal2(self.get_col(),self.get_row()))
        self.attacked_fields.extend(setUp.horizontal_moves(self.get_col(),self.get_row()))
        self.attacked_fields.extend(setUp.vertical_moves(self.get_col(),self.get_row()))
        return self.attacked_fields     

class King(Piece):
    def __init__(self, name, row_number, col_number, team):
        super().__init__(name, row_number, col_number, team)

        




        


