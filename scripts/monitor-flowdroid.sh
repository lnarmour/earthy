#!/bin/bash

# matches the output of tree


function gather {
  for l in log/flowdroid/*.log; 
  do 
    app=`echo $l | sed 's~.*/\(.*\)~\1~'`;
    echo "- $(cat $l | grep 'Found .* leaks' | sed 's~.*\(Found .* leaks\).*~\1~')"; 
  done;
}

function gather_sort {
  echo ""
  echo ""
  gather | sort
  echo ""
  echo ""
}

paste -d ' ' <(tree log) <(gather_sort)
