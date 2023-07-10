## VLDB Vol 16 Formatting
+ Paper length:
  + The maximum paper length is 12 pages for regular research papers, experimental evaluation papers and industry track papers, 8 pages for scalable data science papers, and 6 pages for vision papers. All the content, including any appendices and acknowledgements but excluding the references, must fit on these 12, 8, and 6 pages, respectively. Only the references can extend a paper beyond the page limit, and there is no limit on the number of pages used for them.
  + The maximum paper length is 4 pages for tutorial and demo track papers. All the content must fit on these 4 pages.
  
+ Make sure that you use the most recent version of the template (see https://vldb.org/pvldb/volumes/16/formatting). If your template misses certain required tags/commands, if it shows unbalanced references or if it displays page headers you are probably using an outdated/wrong template.

+ Please make sure that your camera-ready paper follows the formatting guidelines according to the Camera Ready formatting instructions on https://vldb.org/pvldb/volumes/16/formatting which cannot be enforced by the template. Please also check that the paper:

  + contains no citations or footnotes in the Abstract.
  + does not show any footnotes (1,2,3,...) or symbols (*,°,^,<dagger>,...) in the PVLDB Reference Format block (these often come from markings in the title and do not belong in the reference format).
  + has no line overflows, i.e., no widows or orphans (see https://en.wikipedia.org/wiki/Widows_and_orphans).
  + does not spill text into margins (this includes ALL margins including the middle one).
  + does not change the default spacing between figures/tables and textual content (i.e. no negative vspaces).
  + does not use floating figures, tables or images in text, because two-column layouts are not suitable for text wrapping 
  + uses readable fonts in diagrams, figures, tables and other material. In particular, the paper should *NOT* use any font smaller than LaTeX's scriptsize.
  + uses the dedicated Acknowledgement section of the template for making acknowledgements.
  + contains the same author information as in CMT. In particular, the order of the authors must be the same in the paper and in CMT. Also middle names of the authors, if any, must be the same as they are in the paper and in CMT.
  + lists every author in its own author tag. The authors can, as shown in the template sample, share the same affiliations, but every author deserves his/her own author tag! There may not be an Additional Authors section.
  + provides an email address and affiliation for each author on the title page.
  + contains the same Abstract as the one submitted to CMT.
  + uses consistent and scientifically correct citations. For example, proceeding citations should state the authors, title, booktitle, pages, volume, issue, and year.
  + provides last accessed dates for URLs.
  + is PDF/A formatted (please use the PDF/A-2 or a more recent standard). A detailed collection of resources is available here: https://github.com/BU-DiSC/pvldb-pdfa-resources/. Your PDF should successfully pass its PDF/A compliance with at least one of the online tools mentioned in the above link. A key property of a PDF/A compliant PDF is that it embeds all fonts, including Type 1 postscript fonts. One can check this with, for instance, the `Properties' menu of Acrobat Reader (should show `embedded' for each font). One can find various tools that convert PDFs into PDF/A format (and, hence, embed the fonts into the document), but the authors need to make sure that the result is as intended. This is a request by the ACM digital library to improve searchability and long-term preservation of our papers; ACM maintains a FAQ about embedding fonts in TeX.

+ Remove special VLDB category tags, such as '[Experiments and Analysis]', from your paper title on your Camera-Ready version if it contains such a tag.

+ Remove the page numbers in your paper by setting: \vldbpagestyle{empty}

+ Check that the Volume number is 16, the Issue number and the year are the ones provided in the email in your paper's PVLDB Reference Format and copyright blocks.

+ Add a URL pointing to the (code) artifacts of your paper in the \vldbavailabilityurl{} command or leave the command empty if you have been exempted from submitting the artifacts. Providing a link will create a special paragraph in the paper that highlights the availability of your artifacts. Note that the provided "URL_TO_YOUR_ARTIFACTS" in the template is an example and needs to be deleted or replaced. Please do not keep this in your CRC! Please make sure that the artifacts checked during the review process are available through the link you provide (unless exempted from providing artifacts). With the availability badge, PVLDB seeks to give special credit to transparent research papers that make their artifacts available to the community.
For details, please see: https://vldb.org/pvldb/reproducibility

+ Regarding your availability URL, please **make sure that the URL is populated at the time of your CRC submission**, since the issue will not be able to proceed otherwise. We understand that this might be a live repository that might get more updates in the future, but it cannot be empty.

+ Rename your paper to: <pid>-<contact-author-lastname>.pdf (e.g.: p842-miller.pdf). Mind that there is a "p" in your paper's pid and that the lastname is written in lower case letters.

+ Note that both the title of the paper and the list of authors should be the same as shown in CMT. You need to obtain explicit permission from the Program Committee (PC) chairs of the track that your paper belongs to change the title (the removal of VLDB category tags does not count here) or if you want to change the list of authors on your Camera-Ready paper. Forward the approval email from the PC chairs to pvldb16@gmail.com once you receive it. Note that such requests are not routinely granted.

+ Note also that adherence to the formatting guidelines is *strict*. This means that you are not allowed to e.g. change any margins, line spacing, or caption whitespace around figures. Papers modifying any such aspect will be returned for reformatting and will miss their publication slot.

+ Prepare the copyright form according to https://vldb.org/pvldb/volumes/16/formatting
  + Download the copyright form, fill in the required information for your paper and sign it. Note that the copyright needs to be signed manually. A computer-written name is not a signature.
  + Choose option A or B from the form for your paper. One and only one option should be selected.
  + Rename your copyright form to: <pid>-<contact-author-lastname>_Copyright.pdf (e.g.: p842-miller_Copyright.pdf)
  + Email your signed copyright form to us: pvldb16@gmail.com
  + Use the ***Track*** and ***Paper ID*** of your paper in the subject line of your email: "Copyright form <ID> <Track>"

+ Upload the requested CRC version of your paper to CMT and send your copyright via email *before* the camera-ready deadline expires. Note that if we do not receive all your artifacts by the aforementioned deadline for the first round, the paper cannot be considered for publication for the current Issue.


## Metadata
The publication notification email will contain metadata information that will allow you to:
+ set the Issue number in your paper by setting: \vldbissue{<IssueNum>}
+ set the Year in your paper by setting: \vldbyear{<CurrentYear>}

Also, for the initial CR submission please:
+ Leave the \vldbpages{XXX-XXX} untouched for now. We will request you to update it in the second round.
+ Leave the \vldbdoi{XX.XX/XXX.XX} untouched for now. We will request you to update it in the second round.

## Final CR
Note that once all CR of an issue are received you will receive a follow up email with corrections and the pages and doi metadata.

