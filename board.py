from re import X
from pieces import Rook,Queen,Pawn,Bishop,King,Knight
class setUp:
    def __init__(self):
        self.in_check=False
        self.checkmate=False
        
        self.white_captives=[]
        self.black_captives=[]

        white_rook_1 = Rook('r',0,0,'w')
        white_rook_2 = Rook('r',0,7,'w')
        white_knight_1 = Knight('h',0,1,'w')#name is h and stands for horse, k is already taken for king
        white_knight_2 = Knight('h',0,6,'w')
        white_bishop_1 = Bishop('b',0,2,'w')
        white_bishop_2 = Bishop('b',0,5,'w')
        white_queen = Queen('q',0,3,'w')
        white_king = King('k',0,2,'w')
        
        white_pawns = []
        for i in range(8):
            white_pawns.append(Pawn('p',1,i,'w'))
        
        black_rook_1 = Rook('r',7,0,'b')
        black_rook_2 = Rook('r',7,7,'b')
        black_knight_1 = Knight('h',7,1,'b')#name is h and stands for horse, k is already taken for king
        black_knight_2 = Knight('h',7,6,'b')
        black_bishop_1 = Bishop('b',7,2,'b')
        black_bishop_2 = Bishop('b',7,5,'b')
        black_queen = Queen('q',7,3,'b')
        black_king= King('k',7,2,'b')
        
        black_pawns = []
        for i in range(8):
            black_pawns.append(Pawn('p',6,i,'b'))
    
        

        self.board = [
            [white_rook_1, white_knight_1,white_bishop_1, white_queen, white_king, white_bishop_2,
            white_knight_2, white_rook_2],

            [white_pawns[0], white_pawns[1], white_pawns[2], white_pawns[3], white_pawns[4],
             white_pawns[5], white_pawns[6], white_pawns[7]],

            [0, 0, 0,0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, white_bishop_1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],

            [black_pawns[0], black_pawns[1],black_pawns[2], black_pawns[3],black_pawns[4], black_pawns[5],
             black_pawns[6],black_pawns[7]],

            [black_rook_1, black_knight_1,black_bishop_1, black_queen, black_king, black_bishop_2,
            black_knight_2, black_rook_2]
            ]
     # returns all horizonatal fields with coordinates, the piece can move to
    def vertical_moves(self,column,row):
        """the list range will be returned at the end and will contain
        in wich range the piece is allowed to move"""
        
        
        line=(self.board[column])
        team=self.board[column][row].get_team()
        range_interval_piece=[]
        range_piece=[]

        if team =='w':
            range_interval_piece = self.white_move_helper(row,line)
        else:
            range_interval_piece = self.black_move_helper(row,line)#make to array
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            range_piece.append((i,column))
        return range_piece
    #returns alll horizontal fields the piece can move to
    def horizontal_moves(self,column,row):
        line=[]
        team=self.board[column][row].get_team()
        for i in range(8):
            line.append(self.board[i][row])
        
        range_interval_piece=[]
        range_piece=[]

        if team =='w':
            range_interval_piece = self.white_move_helper(column,line)
        else:
            range_interval_piece = self.black_move_helper(column,line)
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            range_piece.append((i,column))
        return range_piece
    #returns diagonal moves
    def diagonal1(self,column,row):
        #diagonal from left top to right bottom
        
        start_row=0
        start_column=0
        range_of_piece=[0,0]
        range_piece=[]
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
        if self.board[column][row].get_team()=='w':
            range_of_piece=self.white_move_helper(position,line)
        else:
            range_of_piece=self.black_move_helper(position,line)
        
        for i in range(range_of_piece[0],range_of_piece[1]+1):
            range_piece.append((start_row+i,start_column+i))

        
        return range_piece
    def diagonal2(self,column,row):
        #diagonal starts at the left bottom to right top
        
        start_row=0
        start_column=7
        range_of_piece=[0,0]
        range_piece=[]
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
        if self.board[column][row].get_team()=='w':
            range_of_piece=self.white_move_helper(position,line)
        else:
            range_of_piece=self.black_move_helper(position,line)
        
        for i in range(range_of_piece[0],range_of_piece[1]+1):
            range_piece.append((start_row+i,start_column-i))

        
        return range_piece
    
    def horse_moves(self,column,row,team):
        #all hores moves(horizontal,vertical)
        moves=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,2)]
        attacks=[]
        for item in moves:
            x=item[0]+row 
            y=item[1]+column 
            if x in range(0,8) and y in range(0,8) and not self.board[y][x].get_team()== team:
                attacks.append[(x,y)]



    def white_move_helper(self,position,line):
        range_of_piece=[0,0]


        left=(line[0:position])
        left.reverse()

        right=line[position+1:8]
        if left:
            for i in range(len(left)):
                if left[i]==0:
                    range_of_piece[0]=(len(left)-1-i)
                    continue
                elif left[i].get_team()=='b':
                    range_of_piece[0]=(len(left)-1-i)#Player can move fields where the opponent is standing
                    break
                elif left[i].get_team()=='w':
                    range_of_piece[0]=(len(left)-i)#Player cant move to fields where an allied figure stands
                    break
        else:
            range_of_piece[0]=(position)
        if right:       
            for i in range(len(right)):
                if right[i]==0:#prblem if no other piece in row
                    range_of_piece[1]=(position+i+1)

                    continue
                elif right[i].get_team()=='b':
                    range_of_piece[1]=(position+i+1)
                    break
                elif right[i].get_team()=='w':
                    range_of_piece[1]=(position+i)
                    break
        else:
            range_of_piece[1]=(position)
        return range_of_piece
    


    def black_move_helper(self,position,line):#problem
        range_of_piece=[0,0]


        left=(line[0:position])
        left.reverse()  

        right=line[position+1:8]
        if left:
            for i in range(len(left)):
                if left[i]==0:
                    range_of_piece[0] = (len(left)-1-i)
                    continue
                elif left[i].get_team()=='w':
                    range_of_piece[0] = (len(left)-1-i)#Player can move fields where the opponent is standing
                    break
                elif left[i].get_team()=='b':
                    range_of_piece[0] = (len(left)-i)#Player cant move to fields where an allied figure stands
                    break
        else:
            range_of_piece = (position)
        if right:       
            for i in range(len(right)):
                if right[i]==0:
                    range_of_piece[1] = (position+i+1)
                    continue
                elif right[i].get_team()=='w':
                    range_of_piece[1] = (position+i+1)
                    break
                elif right[i].get_team()=='b':
                    range_of_piece[1] = (position+i)
                    break
        else:
            range_of_piece[1] = (position)
        return range_of_piece

            

chess=setUp()
#print(chess.horizontal_moves(2,3))
print(chess.diagonal1(4,3))
print(chess.diagonal2(4,3))


                    




        
