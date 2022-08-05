


class Piece:
    def __init__(self,name,row,col,team):
        self.has_moved=False
        self.row = row
        self.col = col
        self.team = team
        self.name=name
        self.check=False
        self.attacked_fields=[]
        self.king_attacks=[]#squares that need to be taken from the opponent to prevent check mate
        self.opponent_team='w'
        if self.team=='w':
            self.opponent_team='b'
        
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    def get_coordinates(self):
        return (self.row,self.col)

    def get_team(self):
        return self.team
    
    def get_opponent_team(self):
        return self.opponent_team
    def get_name(self):
        return self.name
    def get_has_moved(self):
        return self.has_moved


    
    def check(self,setUp):#finds out wether the piece attacks the oponents king
        attacks= self.attacks(setUp)
        for attack in attacks:
            figur=setUp.board[attack[1]][attack[0]]
            if figur!=0 and figur.get_name()=='k' and figur.get_team()==self.get_opponent_team():
                return True
        return False
    def change_row(self,new_row,setUp):
        
        setUp.board[self.col][self.row]=0
        self.row=new_row
        setUp.board[self.col][self.row]=self

    def check_prevention(self):# finds out, if check can be prevented
        return self.king_attacks
    def special_moves(self,moves,prevention):#only viable moves when the team is in check
        valid=[]
        for move in moves:
            if move in prevention:
                valid.append(move)
        return valid
        

            
    def attacks(self,setUp):
        pass
    def get_moves(self,setUp):
        moves=setUp.friendly_fire_preventer(self.attacks(setUp),self.team)
        if setUp.in_check:
            return self.special_moves(moves,setUp.check_prevent)
        else:
            return moves
    

    
    def change_field(self, new_row_num,new_col_num,setUp): #x
        if (new_row_num,new_col_num) in self.get_moves(setUp):
            setUp.board[self.col][self.row]=0
            self.row=new_row_num
            self.col=new_col_num
            self.has_moved=True
            return True
        else:
            return False
    

    


      

class Pawn(Piece):
    def __init__(self, name, row, col, team):
        super().__init__(name, row, col, team)
        
    
    def attacks(self, setUp):
        self.attacked_fields.extend(setUp.pawn_attacks(self.get_col(),self.get_row(),self.get_team()))
        return self.attacked_fields
    
    def check_prevention(self,setUp):
        if self.check(setUp):
            return self.get_coordinates()

    
    def get_moves (self, setUp):
    
     moves=(setUp.pawn_moves(self.attacked_fields,self.get_col(),self.get_row(),self.get_team()))
     if setUp.in_check:
            return self.special_moves(moves,setUp.check_prevent)
     else:
        return moves

class Knight(Piece):
    def __init__(self, name, row, col, team):
        super().__init__(name, row, col, team)
    def attacks(self, setUp):
        self.attacked_fields.extend(setUp.horse_moves(self.get_col(),self.get_row()))
        return self.attacked_fields
    def check_prevention(self,setUp):
        if self.check(setUp):
            return self.get_coordinates()
        
        
        

class Bishop(Piece):
    def __init__(self, name, row, col, team):
        super().__init__(name, row, col, team)

    def attacks(self,setUp):
        diagonal1=(setUp.diagonal1(self.get_col(),self.get_row()))
        diagonal2=(setUp.diagonal2(self.get_col(),self.get_row()))
        self.attacked_fields = diagonal1[0]+diagonal2[0]
        self.king_attacks=diagonal1[1]+diagonal2[1]
        return self.attacked_fields
        
class Rook(Piece):
    def __init__(self, name, row, col, team):
        super().__init__(name, row, col, team)
    def attacks(self, setUp):
        horizontal = (setUp.horizontal_moves(self.get_col(),self.get_row()))
        vertical = (setUp.vertical_moves(self.get_col(),self.get_row()))
        self.attacked_fields=horizontal[0]+vertical[0]
        self.king_attacks=horizontal[1]+vertical[1]
        return self.attacked_fields


    # def attacks(self):
    #     if self.team=='w':
class Queen(Piece):
    def __init__(self, name, row, col, team):
        super().__init__(name, row, col, team)
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
    def __init__(self, name, row, col, team):
        super().__init__(name, row, col, team)
    
    def change_field(self, new_row,new_col,setUp):
        moves=self.get_moves(setUp) 
        right=(self.row+2,self.col)
        left=(self.row-2,self.col)
        if right in moves and right==(new_row,new_col):
            self.castle_right(setUp)
            return True
        elif left in moves and left==(new_row,new_col):
            self.castle_left(setUp)
            return True
        elif (new_row,new_col) in moves:
            setUp.board[self.col][self.row]=0
            self.row=new_row
            self.col=new_col
            self.has_moved=True
            return True
        else:
            return False
        

    
    def attacks(self, setUp):
        return setUp.king_attacks(self.get_col(),self.get_row())
    
    def get_moves (self, setUp):
        
        attacks=self.attacks(setUp)
        
        setUp.board[self.get_col()][self.get_row()]=0
        opponent_attacks=setUp.get_all_attacks(self.get_opponent_team())
        for attack in attacks[:]:
            square=setUp.board[attack[1]][attack[0]]
            if attack in opponent_attacks[:] or square!=0 and square.get_team()==self.get_team():
                attacks.remove(attack)
        setUp.board[self.get_col()][self.get_row()]=self
        if self.castling_left(setUp):
            attacks.append((2,self.col))
        if self.castling_right(setUp):
            attacks.append((6,self.col))
        return attacks

    def castling_right(self,setUp):
        squares=[(self.row+1,self.col),(self.row+2,self.col),self.get_coordinates()]
        opponent_attacks=setUp.get_all_attacks(self.get_opponent_team())
        rook=setUp.board[self.get_col()][7]
        if self.has_moved==False and rook!=0 and rook.get_has_moved()==False:
            if (self.row,self.col) in rook.attacks(setUp) and not bool(set(squares) & set(opponent_attacks)):
                return True
            
        return False

    def castling_left(self,setUp):
        squares=[(self.row-1,self.col),(self.row-2,self.col),self.get_coordinates()]
        opponent_attacks=setUp.get_all_attacks(self.get_opponent_team())
        rook=setUp.board[self.get_col()][0]
        if self.has_moved==False and rook!=0 and rook.get_has_moved()==False:
            if (self.row,self.col) in rook.attacks(setUp) and not bool(set(squares) & set(opponent_attacks)):
                return True
        return False

    def castle_right(self,setUp):
        self.change_row(6,setUp)
        setUp.board[self.get_col()][7].change_row(5,setUp)

    def castle_left(self,setUp):
        self.change_row(2,setUp)
        setUp.board[self.get_col()][0].change_row(3,setUp)

            



            


        

        




        


