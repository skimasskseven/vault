  #!/bin/bash
  echo "Sichere Haupt-Vault..."
  cd ~/Desktop/vault && git add . && git commit -m "auto-sync" && git push

  echo "Sichere Conformis-Notizen..."
  cd ~/Desktop/vault/20_projekte/sa_conformis && git add . && git commit -m "auto-sync" && git push

  echo "Sichere Running-App-Notizen..."
  cd ~/Desktop/vault/20_projekte/app_runningapp && git add . && git commit -m "auto-sync" && git push

  echo "Sichere Research-Monster-Notizen..."
  cd ~/Desktop/vault/20_projekte/research-monster && git add . && git commit -m "auto-sync" && git push

  echo "Sichere PackCheck-Notizen..."
  cd ~/Desktop/vault/20_projekte/sa_packcheck && git add . && git commit -m "auto-sync" && git push

  echo "--- ALLES GESICHERT ---"
  sleep 2
