#!/usr/bin/env python3
"""Hook PreToolUse(Bash) — refuse un `cd <chemin relatif>` en tête de commande.

Motif : le cwd du shell persiste entre deux appels Bash. Après un `cd themes/x/dist`,
un `cd themes/y` écrit comme si l'on était à la racine échoue en `exit 1`. Observé sur
9 sessions distinctes entre 2026-05-30 et 2026-07-31.

Sortie : exit 0 = laisse passer ; exit 2 = bloque et renvoie stderr au modèle.
Volontairement conservateur : n'inspecte que le TOUT DÉBUT de la commande, laisse
passer `cd /abs`, `cd ~…`, `cd "$VAR"`, `cd -` et `cd` seul.
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError):
    sys.exit(0)  # entrée illisible : ne jamais bloquer sur un doute

if data.get("tool_name") != "Bash":
    sys.exit(0)

commande = (data.get("tool_input") or {}).get("command", "")
if not isinstance(commande, str):
    sys.exit(0)

# `cd` en tête de commande uniquement, cible non vide, hors `cd -` et `cd --`.
m = re.match(r"""\s*cd\s+(?!-)(['"]?)([^\s;&|)'"]+)\1""", commande)
if not m:
    sys.exit(0)

cible = m.group(2)
if cible.startswith(("/", "~", "$")):
    sys.exit(0)

print(
    f"`cd {cible}` est un chemin relatif. Le cwd de ce shell persiste entre appels "
    f"et n'est pas forcément la racine du repo — cette commande échouera si le shell "
    f"est resté dans un sous-dossier. Utilise un chemin absolu "
    f"(ou $CLAUDE_PROJECT_DIR/{cible}).",
    file=sys.stderr,
)
sys.exit(2)
