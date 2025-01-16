# 2.0
import tkinter as tk

class Player:
    def __init__(self, label):
        self.label = label
        self.sequence = {i:[0,0] for i in range(3)}
        self.step = 0

class board:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.grid_state = [['' for _ in range(3)] for _ in range(3)]
        self.player_O = Player('O')
        self.player_X = Player('X')
        self.current_player = self.player_O
        self.create_board()
        self.window.mainloop()
    
    def on_click(self, event, row, col):
        idx = self.current_player.step % 3 
        if self.grid_state[row][col] != '':
            label = tk.Label(self.window, text='請選其他位置', font=("Helvetica", 16))
            label.grid(row=3, column=0, columnspan=3)
        else:
            if self.current_player.label == 'O':
                self.clear_dash()
                self.board[row][col].create_oval(20, 20, 80, 80, outline="red", width=4)
                self.next_player = self.player_X if self.current_player == self.player_O else self.player_O
                self.retrieve()
                
            else:
                self.clear_dash()
                self.board[row][col].create_line(20, 20, 80, 80, fill="blue", width=4)
                self.board[row][col].create_line(20, 80, 80, 20, fill="blue", width=4)
                self.next_player = self.player_X if self.current_player == self.player_O else self.player_O
                self.retrieve()
            
            self.grid_state[row][col] = self.current_player.label
            self.current_player.sequence[idx] = [row, col]
            if self.check_winner():
                self.show_winner(message=f'玩家 {self.current_player.label} 獲勝！')
                self.reset_board()
            if self.is_draw():
                self.show_winner(message='平局')
                self.reset_board()
            self.current_player.step += 1
            self.current_player = self.player_X if self.current_player == self.player_O else self.player_O


    def clear_dash(self):
        idx = self.current_player.step % 3
        row, col = self.current_player.sequence[idx]
        if self.current_player.step > 2:
            self.grid_state[row][col]=''
            self.board[row][col].delete('all')        

    def retrieve(self):
        idx = self.next_player.step % 3
        row, col = self.next_player.sequence[idx]
        if self.next_player.step > 2:
            self.grid_state[row][col]='Y'
            if self.current_player.label == 'X':
                self.board[row][col].delete('all')
                self.board[row][col].create_oval(20, 20, 80, 80, outline="red", dash=(4,4), width=4)
            else:
                self.board[row][col].delete('all')
                self.board[row][col].create_line(20, 20, 80, 80, fill="blue", dash=(4,4), width=4)
                self.board[row][col].create_line(20, 80, 80, 20, fill="blue", dash=(4,4), width=4)           
            

    def create_board(self):
        self.window = tk.Tk()
        self.window.title('Tic-Tac-Toe Game')
        for row in range(3):
            for col in range(3):
                # 使用 Canvas 來作為棋盤格子
                canvas = tk.Canvas(self.window, width=100, height=100, bg="white")
                canvas.grid(row=row, column=col)
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.on_click(event, r, c))
                self.board[row][col] = canvas

    def check_winner(self):
        symbol = self.current_player.label
        for i in range(3):
            if self.grid_state[i][0] == self.grid_state[i][1] == self.grid_state[i][2] == symbol:
                return True
            elif self.grid_state[0][i] == self.grid_state[1][i] == self.grid_state[2][i] == symbol:
                return True
        if all(self.grid_state[i][i] == symbol for i in range(3)) or all(self.grid_state[i][2-i] == symbol for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.grid_state[i][j] != '' for i in range(3) for j in range(3)) and not self.check_winner()
    
    def show_winner(self, message):
        # 顯示勝利訊息，並禁用所有按鈕
        for row in range(3):
            for col in range(3):
                self.board[row][col].unbind("<Button-1>")
        result_label = tk.Label(self.window, text=message, font=("Helvetica", 16))
        result_label.grid(row=3, column=0, columnspan=3)
        self.winner_msg = result_label

    def reset_game(self):
        self.grid_state = [['' for _ in range(3)] for _ in range(3)]
        self.player_O = Player('O')
        self.player_X = Player('X')
        self.winner_msg.destroy()
        self.restart_button.destroy()
        for row in range(3):
            for col in range(3):
                # 使用 Canvas 來作為棋盤格子
                canvas = tk.Canvas(self.window, width=100, height=100, bg="white")
                canvas.grid(row=row, column=col)
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.on_click(event, r, c))
                self.board[row][col] = canvas
        self.current_player = self.player_O
        
            
    
    def reset_board(self):
        button = tk.Button(master=self.window, text='重新開始', command=self.reset_game)
        button.grid(row=4, column=0, columnspan=3)
        self.restart_button = button
        

        


if __name__ == '__main__':
    board()