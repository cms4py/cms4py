import config
import tornado.template

loader = tornado.template.Loader(config.TEMPLATES_FOLDER)
