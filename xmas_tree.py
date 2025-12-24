#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
크리스마스 트리와 눈이 내리는 애니메이션
"""

import time
import random
import os
import sys

# ANSI 색상 코드
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BROWN = '\033[38;5;94m'  # 갈색
    DARK_YELLOW = '\033[38;5;130m'  # 진한 노란색 (갈색 대용)
    BRIGHT_RED = '\033[91;1m'
    BRIGHT_GREEN = '\033[92;1m'
    BRIGHT_YELLOW = '\033[93;1m'
    BRIGHT_BLUE = '\033[94;1m'
    BRIGHT_MAGENTA = '\033[95;1m'
    BRIGHT_CYAN = '\033[96;1m'
    BRIGHT_WHITE = '\033[97;1m'
    RESET = '\033[0m'

class ChristmasTree:
    def __init__(self, width=60, height=20):
        self.width = width
        self.height = height
        self.snow_flakes = []
        
    def clear_screen(self):
        """화면 지우기"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def generate_tree(self):
        """크리스마스 트리 생성"""
        tree = []
        center = self.width // 2
        
        # 별 (트리 상단)
        star_colors = [Colors.BRIGHT_YELLOW, Colors.BRIGHT_WHITE, Colors.YELLOW]
        star_color = random.choice(star_colors)
        star_line = " " * center + f"{star_color}*{Colors.RESET}"
        tree.append(star_line)
        
        # 트리 본체 - 3개 섹션 (더 크게)
        sections = [
            {'rows': 4, 'max_width': 9},   # 상단
            {'rows': 5, 'max_width': 15},  # 중단  
            {'rows': 6, 'max_width': 21}   # 하단
        ]
        
        for section in sections:
            for row in range(section['rows']):
                # 각 행의 너비를 점진적으로 증가
                width = 1 + row * 2
                if width > section['max_width']:
                    width = section['max_width']
                
                spaces = center - (width // 2)
                
                # 트리 (기본 문자만, 색상 없음)
                tree_part = '^' * width
                line = " " * spaces + tree_part
                tree.append(line)
        
        # 나무 기둥
        trunk_spaces = center - 1
        for _ in range(2):
            trunk_line = " " * trunk_spaces + "|||"
            tree.append(trunk_line)
        
            
        return tree
    
    def generate_snow(self):
        """눈송이 생성 및 업데이트"""
        # 새로운 눈송이 추가
        if random.random() < 0.6:  # 60% 확률로 새 눈송이 생성
            snow_chars = ['*', '.', 'o', '~']
            snow_colors = [Colors.WHITE, Colors.BRIGHT_WHITE, Colors.CYAN, Colors.BRIGHT_CYAN]
            char = random.choice(snow_chars)
            color = random.choice(snow_colors)
            
            self.snow_flakes.append({
                'x': random.randint(0, self.width - 1),
                'y': 0,
                'char': f"{color}{char}{Colors.RESET}"
            })
        
        # 기존 눈송이 위치 업데이트
        updated_flakes = []
        for flake in self.snow_flakes:
            flake['y'] += 1
            # 좌우로 살짝 흔들림 효과
            if random.random() < 0.3:
                flake['x'] += random.choice([-1, 0, 1])
                flake['x'] = max(0, min(self.width - 1, flake['x']))
            
            # 화면 아래로 떨어지지 않은 눈송이만 유지
            if flake['y'] < self.height - 1:
                updated_flakes.append(flake)
        
        self.snow_flakes = updated_flakes
    
    def render_frame(self):
        """한 프레임 렌더링"""
        tree_lines = self.generate_tree()
        
        # 전체 화면 생성
        screen = []
        for y in range(self.height):
            line = [' '] * self.width
            screen.append(line)
        
        # 트리 그리기
        tree_start_y = 2  # 트리 시작 위치
        for i, tree_line in enumerate(tree_lines):
            y_pos = tree_start_y + i
            if y_pos < self.height:
                for j, char in enumerate(tree_line):
                    if j < self.width and char != ' ':
                        screen[y_pos][j] = char
        
        # 눈송이 그리기
        for flake in self.snow_flakes:
            x, y = flake['x'], flake['y']
            if 0 <= x < self.width and 0 <= y < self.height:
                # 트리와 겹치지 않는 곳에만 눈송이 그리기
                if screen[y][x] == ' ':
                    screen[y][x] = flake['char']
        
        # 화면 출력
        self.clear_screen()
        
        # 제목 출력 (반짝반짝)
        title_colors = [Colors.BRIGHT_RED, Colors.BRIGHT_GREEN, Colors.BRIGHT_YELLOW, Colors.BRIGHT_MAGENTA]
        title_color = random.choice(title_colors)
        title = f"{title_color}*** Merry Christmas Tree ***{Colors.RESET}"
        print(" " * ((self.width - 29) // 2) + title)
        print()
        
        # 프레임 출력 (개별 문자 색칠)
        for line in screen:
            colored_line = ""
            for char in line:
                if char == '^':
                    if random.random() < 0.1:  # 10% 확률로 노란색
                        colored_line += f"{Colors.BRIGHT_YELLOW}^{Colors.RESET}"
                    else:
                        colored_line += f"{Colors.GREEN}^{Colors.RESET}"
                elif char == '|':
                    colored_line += f"{Colors.BROWN}|{Colors.RESET}"
                else:
                    colored_line += char
            print(colored_line)
        
        # 하단 메시지
        message = "\n\n\nSnow falling ~ Press Ctrl+C to exit"
        print(" " * ((self.width - len(message)) // 2) + message)
    
    def animate(self):
        """애니메이션 실행"""
        print("크리스마스 트리 애니메이션을 시작합니다...")
        time.sleep(1)
        
        try:
            while True:
                self.generate_snow()
                self.render_frame()
                time.sleep(0.2)  # 0.2초 간격으로 업데이트
        except KeyboardInterrupt:
            print("\n\n*** Merry Christmas! Happy Holidays! ***")
            sys.exit(0)

def main():
    """메인 함수"""
    tree = ChristmasTree()
    tree.animate()

if __name__ == "__main__":
    main()