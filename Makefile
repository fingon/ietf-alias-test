#
# $Id: Makefile $
#
# Author: Markus Stenberg <fingon@iki.fi>
#
# Created:       Sat Jul 27 11:19:55 2013 mstenber
# Last modified: Sat Jul 27 14:39:25 2013 mstenber
# Edit time:     13 min
#
#

# Assumptions:
# - draft-aliases, wg-aliases downloaded from tools.ietf.org
# - locally installed IETF development database
# - ietf/bin (from IETF tools) in path, appropriate PYTHONPATH set

# => can use these tools to compare results.

TARGETS=draft-aliases.new wg-aliases.new draft-aliases.diff wg-aliases.diff

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

summary: draft-aliases.summary wg-aliases.summary


draft-aliases.new:
	generate-draft-aliases > $@.new
	mv $@.new $@

wg-aliases.new:
	generate-wg-aliases > $@.new
	mv $@.new $@

%.diff: %.new aliasdiff.py
	python aliasdiff.py $* $*.new > $@.new
	mv $@.new $@

%.summary: %.diff
	@echo "Dumping $@"
	@cut -d ' ' -f 1 $< | sort | uniq -c | sort -n
	@echo "Total # of aliases" `cat $*.new | wc -l`
	@echo "Total # of people in aliases" `cat $*.new | perl -pe 's/^.*://' | perl -pe 's/,/\n/g' | wc -l`
