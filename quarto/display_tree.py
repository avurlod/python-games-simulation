def text_of_tree(position, tabs=1) -> str:
    lines = []
    if 1 == tabs:
        lines = [f"Début du jeu, dernière case jouée {position.case_last_played} -- {position.eval}"]
    sep = f"{tabs * '        '}"
    for child in position.children:
        lines_child = []
        lines_child.append(f"{sep}{position.piece} on {child.case_last_played} -- {child.eval}")

        if child.children is not None:
            lines_child.append(text_of_tree(child, tabs+1))
        lines.append(f'\n'.join(lines_child))
        
    return f'\n'.join(lines)
