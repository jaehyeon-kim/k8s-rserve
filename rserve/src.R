test <- function(n, ...) {
    extra_args = unlist(list(...))
    wait = if (is.null(extra_args["wait"])) 0.2 else extra_args["wait"]
    Sys.sleep(wait)
    list(n = n, wait=wait, hostname = system('cat /etc/hostname', intern=TRUE))
}