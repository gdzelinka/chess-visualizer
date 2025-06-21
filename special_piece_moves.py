HIGHLIGHT_COLOR = (124, 252, 0, 128)  # Light green with alpha
SELECTED_COLOR = (255, 255, 0, 128)    # Yellow with alpha
CAPTURE_COLOR = (255, 0, 0, 128)       # Red with alpha for capture squares

def is_path_clear(board, start, end):
    """Check if the path between two squares is clear of pieces."""
    start_row, start_col = start
    end_row, end_col = end

    # Determine direction of movement
    row_dir = 0 if start_row == end_row else (1 if end_row > start_row else -1)
    col_dir = 0 if start_col == end_col else (1 if end_col > start_col else -1)

    # Check each square along the path
    current_row, current_col = start_row + row_dir, start_col + col_dir
    while (current_row, current_col) != (end_row, end_col):
        if (current_row, current_col) in board:
            return False
        current_row += row_dir
        current_col += col_dir
    return True

def is_valid_position(board_size, pos):
    row, col = pos
    return 0 <= row < board_size and 0 <= col < board_size

def jump_moves_filter(board, square, color, moves_with_info):
    start_row, start_col = square
    ORIGIN_DIRECTION = {}
    filtered_moves = []
    for move, can_jump in moves_with_info:
        if isinstance(can_jump, tuple) and can_jump[0] == 'origin':
            target_board_result = board.get(move)
            if target_board_result:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
            if target_board_result is None:
                ORIGIN_DIRECTION[can_jump[1]] = move
                filtered_moves.append((move, HIGHLIGHT_COLOR))
            elif target_color != color:
                filtered_moves.append((move, CAPTURE_COLOR))
    for move, can_jump in moves_with_info:
        if isinstance(can_jump, tuple) and can_jump[0] == 'direction':
            end_row, end_col = move
            if can_jump[1] in ORIGIN_DIRECTION.keys():
                move = (ORIGIN_DIRECTION[can_jump[1]][0] + end_row - start_row, ORIGIN_DIRECTION[can_jump[1]][1] + end_col - start_col)
                target_board_result = board.get(move)
                if target_board_result:
                    target_piece_key, _ = target_board_result
                    target_color = target_piece_key.split('_')[0]
                else:
                    target_color = None
                if target_board_result is None:
                    filtered_moves.append((move, HIGHLIGHT_COLOR))
                elif target_color != color:
                    filtered_moves.append((move, CAPTURE_COLOR))
                    ORIGIN_DIRECTION.pop(can_jump[1], None)
        else:
            target_board_result = board.get(move)
            if target_board_result:
                target_piece_key, _ = target_board_result
                target_color = target_piece_key.split('_')[0]
            else:
                target_color = None
            if target_board_result is None:
                # Empty square, check if path is clear or if piece can jump
                if can_jump == True or is_path_clear(board, square, move):
                    filtered_moves.append((move, HIGHLIGHT_COLOR))

            elif target_color != color:  # Different color piece
                if can_jump == True or is_path_clear(board, square, move):
                    filtered_moves.append((move, CAPTURE_COLOR))
    return filtered_moves

def is_path_clear_for_royal_piece(board, start, end, piece_rank):
    """Check if the path between two squares is clear for Royal pieces, allowing jumps over pieces ranked below."""
    start_row, start_col = start
    end_row, end_col = end

    # Determine direction of movement
    row_dir = 0 if start_row == end_row else (1 if end_row > start_row else -1)
    col_dir = 0 if start_col == end_col else (1 if end_col > start_col else -1)

    # Check each square along the path
    current_row, current_col = start_row + row_dir, start_col + col_dir
    while (current_row, current_col) != (end_row, end_col):
        if (current_row, current_col) in board:
            # Get the rank of the piece in the way
            blocking_piece = board[(current_row, current_col)]
            blocking_piece_key, blocking_rank = blocking_piece

            if blocking_rank >= piece_rank:
                return False  # Cannot jump over this piece
        current_row += row_dir
        current_col += col_dir
    return True

def royal_moves_filter(board, square, color, rank, moves_with_info):
    start_row, start_col = square
    filtered_moves = []

    for move, can_jump in moves_with_info:
        target_board_result = board.get(move)
        if target_board_result:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
        else:
            target_color = None
        if is_path_clear_for_royal_piece(board, square, move, rank):
            if target_board_result is None:
                filtered_moves.append((move, HIGHLIGHT_COLOR))
            else:
                filtered_moves.append((move, CAPTURE_COLOR))
    return filtered_moves

def highlight_turned_squares(board, board_size, start, end, color):
    highlighted_turned_moves = []
    start_row, start_col = start
    end_row, end_col = end

    x_delta = end_col - start_col
    y_delta = end_row - start_row

    if x_delta == 0 and y_delta != 0: # Moving up or down
        #Highlight the squares to the left and right of the end square
        move = (end_row, end_col - 1)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0], move[1] - 1)
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
        move = (end_row, end_col + 1)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0], move[1] + 1)
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
    elif x_delta != 0 and y_delta == 0: # Moving right or left
        move = (end_row - 1, end_col)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0] - 1, move[1])
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
        move = (end_row + 1, end_col)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0] + 1, move[1])
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
    elif (x_delta < 0 and y_delta < 0) or (x_delta > 0 and y_delta > 0): # Moving diagonally
        move = (end_row - 1, end_col + 1)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0] - 1, move[1] + 1)
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
        move = (end_row + 1, end_col - 1)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0] + 1, move[1] - 1)
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
    elif (x_delta < 0 and y_delta > 0) or (x_delta > 0 and y_delta < 0): # Moving diagonally
        move = (end_row + 1, end_col + 1)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0] + 1, move[1] + 1)
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
        move = (end_row - 1, end_col - 1)
        target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        while is_valid_position(board_size, move) and target_board_result is None:
            highlighted_turned_moves.append((move, HIGHLIGHT_COLOR))
            move = (move[0] - 1, move[1] - 1)
            target_board_result = board.get(move) if is_valid_position(board_size, move) else None
        if is_valid_position(board_size, move) and target_board_result is not None:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            if target_color != color:
                highlighted_turned_moves.append((move, CAPTURE_COLOR))
    return highlighted_turned_moves

def hook_moves_filter(board, board_size, square, color, moves_with_info):
    filtered_moves = []

    for move, can_jump in moves_with_info:
        target_board_result = board.get(move)
        if target_board_result:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
        else:
            target_color = None
        if target_board_result is None:
            if is_path_clear(board, square, move):
                filtered_moves.append((move, HIGHLIGHT_COLOR))
            if can_jump:
                highlighted_turned_moves = highlight_turned_squares(board, board_size, square, move, color)
                filtered_moves.extend(highlighted_turned_moves)
        elif target_color != color:
            if is_path_clear(board, square, move):
                filtered_moves.append((move, CAPTURE_COLOR))
    return filtered_moves

def highlight_jumpable_squares(board, square, move, color, limit, pieces_jumped_per_direction):
    # Pieces Jumped per direction:
    # 0: Down
    # 1: Up
    # 2: Left
    # 3: Right
    # 4: Diagonally up left
    # 5: Diagonally up right
    # 6: Diagonally down left
    # 7: Diagonally down right
    highlighted_jumpable_moves = []
    start_row, start_col = square
    end_row, end_col = move
    x_delta = end_col - start_col
    y_delta = end_row - start_row
    target_board_result = board.get(move)
    if x_delta == 0 and y_delta > 0: # Moving down
        if target_board_result is None and pieces_jumped_per_direction[0] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[0] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[0] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))

    elif x_delta == 0 and y_delta < 0: # Moving up
        if target_board_result is None and pieces_jumped_per_direction[1] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[1] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[1] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    elif x_delta < 0 and y_delta == 0: # Moving left
        if target_board_result is None and pieces_jumped_per_direction[2] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[2] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[2] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    elif x_delta > 0 and y_delta == 0: # Moving right
        if target_board_result is None and pieces_jumped_per_direction[3] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[3] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[3] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    elif (x_delta < 0 and y_delta < 0): # Moving diagonally up left
        if target_board_result is None and pieces_jumped_per_direction[4] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[4] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[4] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    elif (x_delta < 0 and y_delta > 0): # Moving diagonally up right
        if target_board_result is None and pieces_jumped_per_direction[5] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[5] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[5] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    elif (x_delta > 0 and y_delta < 0): # Moving diagonally down left
        if target_board_result is None and pieces_jumped_per_direction[6] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[6] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[6] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    elif (x_delta > 0 and y_delta > 0): # Moving diagonally down right
        if target_board_result is None and pieces_jumped_per_direction[7] <= limit:
            highlighted_jumpable_moves.append((move, HIGHLIGHT_COLOR))
        elif target_board_result is not None and pieces_jumped_per_direction[7] <= limit:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
            pieces_jumped_per_direction[7] += 1
            if target_color != color:
                highlighted_jumpable_moves.append((move, CAPTURE_COLOR))
    return highlighted_jumpable_moves

def limited_jumping_moves_filter(board, square, color, moves_with_info):
    pieces_jumped_per_direction = [0, 0, 0, 0, 0, 0, 0, 0]
    start_row, start_col = square
    filtered_moves = []
    for move, can_jump in moves_with_info:
        target_board_result = board.get(move)
        if target_board_result:
            target_piece_key, _ = target_board_result
            target_color = target_piece_key.split('_')[0]
        else:
            target_color = None
        if isinstance(can_jump, tuple) and can_jump[0] == 'limited_jumping':
            highlighted_jumpable_moves = highlight_jumpable_squares(board, square, move, color, can_jump[1], pieces_jumped_per_direction)
            filtered_moves.extend(highlighted_jumpable_moves)
        else:
            if target_board_result is None:
                if can_jump or is_path_clear(square, move):
                    filtered_moves.append((move, HIGHLIGHT_COLOR))
            elif target_color != color:
                if can_jump == True or is_path_clear(square, move):
                    filtered_moves.append((move, CAPTURE_COLOR))
    return filtered_moves
