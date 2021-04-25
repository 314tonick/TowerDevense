n, m = map(int, input().split())
words = {}
commands = [0] * n
for _ in range(m):
    c, w = input().split()
    words[w] = int(c)
for k, v in words.items():
    commands[v-1] += 1
print(*commands)
