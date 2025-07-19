/*
 * MIT License
 *
 * Copyright (c) 2025 https://yunp.top
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 * Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
 * AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
 * THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package top.yunp.cms4py.framework.web;

interface IWebConfig {
    public var serverPort:Int;
    public var staticRoot:String;
    public var templateRoot:String;
    public var db:String;
    public var dbHost:String;
    public var dbPort:Int;
    public var dbUser:String;
    public var dbPassword:String;
    public var dbName:String;
    public var dbPoolMinsize:Int;
    public var dbPoolMaxsize:Int;
    public var workers:Int;
    public var logLevel:String;
    public var logLevelIndex:Int;
    public var siteName:String;
    public var sessionJwtName:String;
    public var sessionJwtSecret:String;

    /**
    Session age, in seconds
    **/
    public var sessionAge:Int;
}
