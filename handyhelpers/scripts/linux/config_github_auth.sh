git config --global user.name notebook
git config --global user.email notebook@email.com

cat > ~/.ssh/id_ed25519 << EOF
{YOUR_PRIVATE_KEY}
EOF

cat > ~/.ssh/config << EOF
Host *
    StrictHostKeyChecking no
EOF

chmod 400 ~/.ssh/id_ed25519
chmod 400 ~/.ssh/config