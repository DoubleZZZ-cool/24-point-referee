import tkinter as tk
from tkinter import ttk

# 创建Tkinter主窗口
root = tk.Tk()
root.title("24-Point Game")

# 扑克选项 (A=1, 2-10, J=11, Q=12, K=13)
card_display_values = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
card_actual_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}

# 初始化四个下拉菜单变量
card1 = tk.StringVar()
card2 = tk.StringVar()
card3 = tk.StringVar()
card4 = tk.StringVar()

# 定义solve函数的回调
def solve_24_point():
    # 获取选择的卡片值并将其转换为整数列表
    selected_cards = [card_actual_values[card1.get()], card_actual_values[card2.get()], card_actual_values[card3.get()], card_actual_values[card4.get()]]
    
    # 调用solve函数并展示结果
    result = solve(selected_cards)
    if result:
        result_label.config(text=f"Solution: {result}", font=("Arial", 14, "bold"))  # 修改字体样式
    else:
        result_label.config(text="No solution found!", font=("Arial", 14, "bold"))

# 创建并放置四个下拉菜单
ttk.Label(root, text="Card 1").grid(column=0, row=0, padx=10, pady=10)
dropdown1 = ttk.Combobox(root, textvariable=card1, values=card_display_values, state='readonly')
dropdown1.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Card 2").grid(column=0, row=1, padx=10, pady=10)
dropdown2 = ttk.Combobox(root, textvariable=card2, values=card_display_values, state='readonly')
dropdown2.grid(column=1, row=1, padx=10, pady=10)

ttk.Label(root, text="Card 3").grid(column=0, row=2, padx=10, pady=10)
dropdown3 = ttk.Combobox(root, textvariable=card3, values=card_display_values, state='readonly')
dropdown3.grid(column=1, row=2, padx=10, pady=10)

ttk.Label(root, text="Card 4").grid(column=0, row=3, padx=10, pady=10)
dropdown4 = ttk.Combobox(root, textvariable=card4, values=card_display_values, state='readonly')
dropdown4.grid(column=1, row=3, padx=10, pady=10)

# 创建并放置"Submit"按钮
submit_button = ttk.Button(root, text="Submit", command=solve_24_point)
submit_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

# 创建显示结果的标签
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=5, columnspan=2, padx=10, pady=10)

# 运行Tkinter主循环
root.mainloop()
