#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"

echo "Building hashcount..."
cd "$ROOT_DIR/hashcount"
mkdir -p build && cd build
cmake -DCLINGO_BUILD_SHARED=ON ..
make -j12
cp hashcount "$ROOT_DIR/scripts"

echo "Building treedecom..."
cd "$ROOT_DIR/treedecom"
./setupdev.sh
cp bin/td "$ROOT_DIR/scripts"
cp bin/flow_cutter_pace17 "$ROOT_DIR/scripts"

echo "Done. Copied binaries to:"
echo "  $ROOT_DIR/scripts/hashcount"
echo "  $ROOT_DIR/scripts/td"
echo "  $ROOT_DIR/scripts/flow_cutter_pace17"