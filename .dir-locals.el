;;; .dir-locals.el
;;
;; Per-Directory Local Variables:
;;   https://www.gnu.org/software/emacs/manual/html_node/emacs/Directory-Variables.html
;;
;; prj-root --> <repo>/
;;   Project's root folder is where the `.dir-locals.el' is located
;;
;; cdb-tools-root --> d:/darmarIT/cdb-tools
;;   Where your cdb-tools are located
;;
;; cdb-tools-ide --> d:/darmarIT/cdb-tools/winShortcuts
;;   If you have an alternative folder for the shortcuts
;;

((nil
  . ((fill-column . 80)
     (indent-tabs-mode . nil)
     (eval . (progn

	       ;; Where your cdb-tools are located
               (setq-local cdb-tools-root
			   (file-name-as-directory "d:/darmarIT/cdb-tools"))

	       ;; If you have an alternative folder for the shortcuts
	       (setq-local cdb-tools-ide
			   (file-name-as-directory "d:/darmarIT/cdb-tools/TEST"))

	       ;; Project's root folder is where the `.dir-locals.el' is located
               (setq-local prj-root
			   (locate-dominating-file default-directory ".dir-locals.el"))

           ))))

 (python-mode
  . ((indent-tabs-mode . nil)

     (eval . (progn

	       (setq-local python-shell-interpreter
			   (concat cdb-tools-ide ".ide-powerscript.bat"))
	       (setq-local python-shell-interpreter-args
			   "--nologin")
	       (setq-local pylint-command
			   (concat cdb-tools-ide ".ide-pylint.bat"))
	       (setq-local pylint-rcfile
			   (concat cdb-tools-root ".pylintrc"))
	       (setq-local pylint-options
			   (list (format "--rcfile=%s" pylint-rcfile)
				 "--reports=y"
				 "--output-format=parseable"
				 (if (eq system-type 'windows-nt)
				     ;; win needs quotation mark
				     "\"--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}\""
				   "--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}'"
				   )
				 ))
	       (setq-local flycheck-python-pylint-executable
			   python-shell-interpreter)

	       (setq-local flycheck-pylintrc
			   pylint-rcfile)
	       ))))
 )
