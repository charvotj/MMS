% !TeX encoding = UTF-8
%% Třída "protokol.cls" vychází ze souboru praktikum.cls
%% od Petra Sadovského (http://fyzika.feec.vutbr.cz/~petrsad/),
%% který v roce 2008 upravil Daniel Horák
%% (http://disk.jabbim.cz/horada@jabbim.cz/sablona_protokolu_univerzalni.zip).
%% V roce 2009 mírně upravil a převedl zpět do CP1250 Pavel Rajmic
%% (http://latex.feec.vutbr.cz/)

%% Některé příkazy z původní třídy nejsou využity (například \ucitel{}
%% Hlavička je trochu upravena pro obecnější použití
%% (název školy, předmětu a ústavu se nastavují přímo v dokumentu
%% patřičnými příkazy)

%% Kódování se předpokládá CP1250, aby bylo možno pohodlně pracovat s TeXnicCenter.

%% Hlavička původního souboru  %%%%%%%%%%%%%%%%
%%
%% This is file `praktikum.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% praktikum.dtx  (with options: `class')
%% 
%% Copyright (C) 2004 
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
%\ProvidesClass{praktikum}
%   [2004/02/14 Document class for Phisical Practicum Proceeding]
\LoadClass[a4paper,onecolumn,12pt]{article}
\usepackage[czech]{babel}
%\usepackage{czech}
\usepackage[utf8]{inputenc}
%\usepackage[T1]{fontenc}
\usepackage{calc}
%\usepackage{layout}
\usepackage{graphicx}   

%nastaveni tiskoveho zrcadla
\setlength{\textwidth}{\paperwidth-5cm}
\setlength{\textheight}{\paperheight-5cm}
\setlength{\hoffset}{2.5cm-1in} 
\setlength{\voffset}{2.5cm-1in}
\setlength{\oddsidemargin}{0pt} 
\setlength{\evensidemargin}{0pt}
\setlength{\topmargin}{-1.2cm}
\setlength{\headsep}{-\topmargin-\headheight}
\setlength{\marginparsep}{5pt} 
\setlength{\marginparwidth}{2cm}

% \setcounter{secnumdepth}{-1}

% \pagestyle{empty}

\hfuzz = 1pt
\tolerance = 1000
\widowpenalty = 10000
\clubpenalty = 8000

\def\@jmeno{}
\def\@kod{}
\def\@rocnik{}
\def\@obor{}
\def\@skupina{}
\def\@labskup{}
\def\@spolupracoval{}
\def\@ucitel{}
\def\@merenodne{}
\def\@odevzdanodne{}
\def\@priprava{}
\def\@opravy{}
\def\@nazev{}
\def\@cislo{}
\def\@predmet{}
\def\@ustav{}
\def\@skola{}

\def\jmeno #1{\def\@jmeno{#1}}
\def\kod #1{\def\@kod{#1}}
\def\rocnik #1{\def\@rocnik{#1}}
\def\obor #1{\def\@obor{#1}}
\def\skupina #1{\def\@skupina{#1}}
\def\labskup #1{\def\@labskup{#1}}
\def\spolupracoval #1{\def\@spolupracoval{#1}}
\def\ucitel #1{\def\@ucitel{#1}}
\def\merenodne #1{\def\@merenodne{#1}}
\def\odevzdanodne #1{\def\@odevzdanodne{#1}}
\def\priprava #1{\def\@priprava{#1}}
\def\opravy #1{\def\@opravy{#1}}
\def\nazev #1{\def\@nazev{#1}}
\def\cislo #1{\def\@cislo{#1}}
\def\predmet #1{\def\@predmet{#1}}
\def\ustav #1{\def\@ustav{#1}}
\def\skola #1{\def\@skola{#1}}

\def\hposuna{\hspace*{-2\fboxrule}}
\def\hposunb{\hspace*{-4\fboxrule}}
\def\hposunc{\hspace*{-1\fboxrule}}
\def\hposund{\hspace*{-5\fboxrule}}
\def\vposuna{\vspace*{-2\fboxrule}}
\def\vposunb{\vspace*{-1.25\fboxrule}}
\def\vposunc{\vspace*{+1.25\fboxrule}}

\renewcommand{\maketitle}{%
	\begin{center}%
		\fboxrule=1mm%
		\fbox{\parbox[t][4,4cm]{16cm}{%
				\vposuna\hposuna\fbox{\parbox[b][1,8cm][c]{10cm}{%
						\begin{center}%
							\large{\mbox{\textbf{\@predmet}}}\par\textbf{\@ustav}\par \@skola%
				\end{center}}}%
				\vposunb%
				\fboxrule=0.35mm%
				\hposunc%
				\fbox{\parbox[b][1,85cm][c]{5,675cm}{%
						\hposunb\fbox{\parbox[t][0,875cm]{3,675cm}{%
								\raggedright{\footnotesize{\textbf{Jméno}}}\par%
								\raggedleft{\textbf{\@jmeno}}}}%
						\hposunc\fbox{\parbox[t][0,875cm]{1,75cm}{%
								\raggedright{\footnotesize{ID}}\par\raggedleft{\textbf{\@kod}}}}%
						\vposuna\par%
						\hposunb\vposuna\fbox{\parbox[t][0,75cm]{1,68cm}{%
								\raggedright{\footnotesize{Ročník}}\par\raggedleft{\@rocnik}}}%
						\hposunc\fbox{\parbox[t][0,75cm]{1,75cm}{%
								\raggedright{\footnotesize{Obor}}\par\raggedleft{\@obor}}}%
						\hposunc\fbox{\parbox[t][0,75cm]{1,75cm}{%
								\raggedright{\footnotesize{Skupina}}\par\raggedleft{\@skupina}}}%
						\par}}\\%
				\vposuna\hposunb\fbox{\parbox[b][0,8cm][c]{16cm}{%
						\hposunb\fbox{\parbox[t][0,8cm]{3,856cm}{%
								\raggedright{\footnotesize{Spolupracoval}}\par\raggedleft{\@spolupracoval}}}%
						\hposunc\fbox{\parbox[t][0,80cm]{3,856cm}{%
								\raggedright{\footnotesize{Měřeno dne}}\par\raggedleft{\@merenodne}}}%
						\hposunc\fbox{\parbox[t][0,80cm]{3,856cm}{%
								\raggedright{\footnotesize{Odevzdáno dne}}\par\raggedleft{\@odevzdanodne}}}%
						\hposunc\fbox{\parbox[t][0,8cm]{3,7cm}{%
								\raggedright{\footnotesize{\textbf{Hodnocení}}}}}
						\par}} %
				
				\fboxrule=1mm%
				\par\hposuna\fbox{\parbox[b][1,2cm][t]{14cm}{%
						\raggedright{\footnotesize{Název zadání}}\par\centering{\Large{\textbf{\@nazev}}}}}%
				\hposunc\fbox{\parbox[b][1,2cm][t]{1,675cm}{%
						\centering{\footnotesize{Č. úlohy}}\par\centering{\large{\textbf{\@cislo}}}}}\par%
		}}%
	\end{center}%
\setlength{\parskip}{5pt}
}

\catcode`\"=\active
\def"{\bgroup\quotedblbase\def"{\textquotedblleft\egroup}}

%\newcommand{\uv}[1]{\raisebox{-1.3ex}[0ex][0ex]{''}\kern-.1ex#1\kern-.1ex``}

\AtBeginDocument{\catcode`\"=\active} %ihned na zacatku dokumentu se provede
\endinput



%% Definice prikazu pro sazbu jednotek
\DeclareMathAlphabet{\jedn}{OT1}{cmr}{m}{n}


%%
%% End of file `praktikum.cls'. 
