#!/bin/bash

# matches the output of tree


function gather {
  for l in log/flowdroid/*.log; 
  do 
    app=`echo $l | sed 's~.*/\(.*\)~\1~'`;
    if [[ -n "$DEBUG" ]]; then debug_app="  ($app)"; else debug_app=""; fi;
    echo "- $(cat $l | grep 'Found .* leaks' | sed "s~.*\(Found .* leaks\).*~\1$debug_app~")"; 
  done;
}

function match_tree {
  echo ""
  echo ""
  gather
  echo ""
  echo ""
}

paste -d ' ' <(tree log) <(match_tree)
