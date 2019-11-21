#!/bin/bash

echo 'Content-Type:text/html'
echo
echo '<html>'
echo '<body>'
echo `pwd`
echo '</body>'
echo '</html>'
>&2 echo test
