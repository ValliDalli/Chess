from re import X
from pieces import Rook,Queen,Pawn,Bishop,King,Knight
class setUp:
    def __init__(self):
        self.in_check=False
        self.checkmate=False
        
        self.white_captives=[]
        self.black_captives=[]

        white_rook_1 = Rook('r',0,0,'w')
        white_rook_2 = Rook('r',7,0,'w')
        white_knight_1 = Knight('h',1,0,'w')#name is h and stands for horse, k is already taken for king
        white_knight_2 = Knight('h',6,0,'w')
        white_bishop_1 = Bishop('b',2,0,'w')
        white_bishop_2 = Bishop('b',5,0,'w')
        white_queen = Queen('q',3,0,'w')
        white_king = King('k',2,0,'w')
        
        white_pawns = []
        for i in range(8):
            white_pawns.append(Pawn('p',i,1,'w'))
        
        black_rook_1 = Rook('r',7,0,'b')
        black_rook_2 = Rook('r',7,7,'b')
        black_knight_1 = Knight('h',7,1,'b')#name is h and stands for horse, k is already taken for king
        black_knight_2 = Knight('h',7,6,'b')
        black_bishop_1 = Bishop('b',7,2,'b')
        black_bishop_2 = Bishop('b',7,4,'b')
        black_queen = Queen('q',7,3,'b')
        black_king= King('k',7,2,'b')
        
        black_pawns = []
        for i in range(8):
            black_pawns.append(Pawn('p',i,6,'b'))
    
        

        self.board = [
            [white_rook_1, white_knight_1,white_bishop_1, white_queen, white_king, white_bishop_2,
            white_knight_2, white_rook_2],

            [white_pawns[0], white_pawns[1], white_pawns[2], white_pawns[3], white_pawns[4],
             white_pawns[5], white_pawns[6], white_pawns[7]],

            [0, 0, 0,0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],

            [black_pawns[0], black_pawns[1],black_pawns[2], black_pawns[3],black_pawns[4], black_pawns[5],
             black_pawns[6],black_pawns[7]],

            [black_rook_1, black_knight_1,black_bishop_1, black_queen, black_king, black_bishop_2,
            black_knight_2, black_rook_2]
            ]

     
    def friendly_fire_preventer(self,attacks,team):
        
        for item in (attacks[:]):
            if self.board[item[1]][item[0]].get_team()==team:
                attacks.remove(item)
        return attacks

        # returns all horizonatal fields with coordinates, the piece can move to
    def vertical_moves(self,column,row):
        """the list range will be returned at the end and will contain
        in wich range the piece is allowed to move"""
        
        
        line=(self.board[column])
        range_interval_piece=[0,0]
        attacks=[]

        
        range_interval_piece = self.move_helper(row,line)
        
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            attacks.append((i,column))
        return attacks
    
    


    #returns alll horizontal fields the piece can move to
    def horizontal_moves(self,column,row):
        line=[0,0]
        for i in range(8):
            line.append(self.board[i][row])
        
        range_interval_piece=[]
        attacks=[]

        range_interval_piece = self.move_helper(row,line)
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            attacks.append((i,column))
        return attacks
    #returns diagonal moves
    def diagonal1(self,column,row):
        #diagonal from left top to right bottom
        
        start_row=0
        start_column=0
        range_interval_piece=[0,0]
        attacks=[]
        if row>column:
            start_row=row-column
        elif row<column:
            start_column=column-row
        position=row-start_row
        a=start_row# just to not change start_row and start column with the wihile lookp
        b=start_column
        #start position helps to get the full diagonal
        line=[]
        while a<=7 and b<=7:
            line.append(self.board[b][a])
            b+=1
            a+=1
        range_interval_piece = self.move_helper(position,line)
        
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            attacks.append((start_row+i,start_column+i))

        
        return attacks
    def diagonal2(self,column,row):
        #diagonal starts at the left bottom to right top
        
        start_row=0
        start_column=7
        range_interval_piece=[0,0]
        attacks=[]
        if row+column<7:
            start_column=row+column
            
        elif row+column>7:
            start_row=row-(7-column)
        position=row-start_row
        a=start_row# just to not change start_row and start column with the wihile lookp
        b=start_column
        #start position helps to get the full diagonal
        line=[]
        while a<=7 and b>=0:
            line.append(self.board[b][a])
            b-=1
            a+=1
        range_interval_piece = self.move_helper(position,line)
        
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            attacks.append((start_row+i,start_column-i))

        
        return attacks
    
    def horse_moves(self,column,row,team):
        #all hores moves(horizontal,vertical)
        moves=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,2)]
        attacks=[]
        for item in moves:
            x=item[0]+row 
            y=item[1]+column 
            if x in range(0,8) and y in range(0,8) and not self.board[y][x].get_team()== team:
                attacks.append((x,y))
    '''fields that are being attacked by the pawn, but may not be movable'''
    def pawn_attacks(self,column,row,team):
        attacks=[]
        if team=='w':
            if column+1<8 and row+1<8:
                attacks.append((row+1,column+1))
            if column+1<8 and row-1<=0:
                attacks.append((row-1,column+1))
        elif team =='b':
            if column-1<=0 and row+1<8:
                attacks.append((row+1,column-1))
            if column-1<=0 and row-1<=0:
                attacks.append((row-1,column-1))
        return attacks
    
    def move_helper(self, position,line):
        range_of_piece=[0,0]

        left=(line[0:position])
        left.reverse()

        right=line[position+1:8]
        if left:
            for i in range(len(left)):
                if left[i]==0:
                    range_of_piece[0]=(len(left)-1-i)
                    continue
                else:
                    range_of_piece[0]=(len(left)-1-i)#Player can move fields where the opponent is standing
                    break
        else:
            range_of_piece[0]=(position)
        if right:       
            for i in range(len(right)):
                if right[i]==0:#prblem if no other piece in row
                    range_of_piece[1]=(position+i+1)

                    continue
                else:
                    range_of_piece[1]=(position+i+1)
                    break
        else:
            range_of_piece[1]=(position)
        return range_of_piece


            

chess=setUp()
#print(chess.horizontal_moves(2,3))
print(chess.board[4][3].attacks(chess))


                    




        
