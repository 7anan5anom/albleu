#!/usr/bin/perl -w

use strict;

my $filename = $ARGV[0];           # store the 1st argument into the variable
open my $fh, '<', $filename or die $!; # open the file using lexically scoped filehandle

while( my $line = <$fh>)  {
#    print "$line\n";
    my $val = NormalizeText ($line);
    print "$val\n";
}

use vars qw ($opt_r $opt_s $opt_t $opt_d $opt_h $opt_b $opt_n $opt_c $opt_x);
my $preserve_case = defined $opt_c ? 1 : 0;

sub NormalizeText {
    my ($norm_text) = @_;
    
    # language-independent part:
    $norm_text =~ s/<skipped>//g; # strip "skipped" tags
    $norm_text =~ s/-\n//g; # strip end-of-line hyphenation and join lines
#    $norm_text =~ s/\p{Hyphen}\p{Zl}//g;
    $norm_text =~ s/\n/ /g; # join lines
    $norm_text =~ s/&quot;/"/g;  # convert SGML tag for quote to "
    $norm_text =~ s/&amp;/&/g;   # convert SGML tag for ampersand to &
    $norm_text =~ s/&lt;/</g;    # convert SGML tag for less-than to >
    $norm_text =~ s/&gt;/>/g;    # convert SGML tag for greater-than to <
    
    # language-dependent part (assuming Western languages):
    $norm_text = " $norm_text ";
    $norm_text =~ tr/[A-Z]/[a-z]/ unless $preserve_case;
    $norm_text =~ s/([\{-\~\[-\` -\&\(-\+\:-\@\/\-])/ $1 /g;   # tokenize punctuation
#        $norm_text =~ s/([^[:ascii:]])/ $1 /g;
        $norm_text =~ s/([^0-9])([\.,])/$1 $2 /g; # tokenize period and comma unless preceded by a digit
        $norm_text =~ s/([^0-9]+)([\.,])([0-9]+)/$1 $2 $3 /g; # tokenize period and comma unless preceded by a digit

        $norm_text =~ s/([0-9]+)([\.,])([^0-9]+)/$1 $2 $3 /g; # tokenize period and comma unless preceded by a digit
        
        $norm_text =~ s/([0-9])(-)/$1 $2 /g; # tokenize dash when preceded by a digit
        $norm_text =~ s/\s+/ /g; # one space only between words
        $norm_text =~ s/^\s+//;  # no leading space
        $norm_text =~ s/\s+$//;  # no trailing space
        
        return $norm_text;
    }
        
        