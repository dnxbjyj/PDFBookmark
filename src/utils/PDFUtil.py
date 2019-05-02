# coding:utf-8
# PDF�ĵ�������
from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer
import os

class PDFHandleMode(object):
    '''
    ����PDF�ļ���ģʽ
    '''
    # ����ԴPDF�ļ����������ݺ���Ϣ���ڴ˻������޸�
    COPY = 'copy'
    # ������ԴPDF�ļ���ҳ�����ݣ��ڴ˻������޸�
    NEWLY = 'newly'

class MyPDFHandler(object):
    '''
    ��װ��PDF�ļ�������
    '''
    def __init__(self,pdf_file_path,mode = PDFHandleMode.COPY):
        '''
        ��һ��PDF�ļ���ʼ��
        :param pdf_file_path: PDF�ļ�·��
        :param mode: ����PDF�ļ���ģʽ��Ĭ��ΪPDFHandleMode.COPYģʽ
        '''
        # ֻ����PDF����
        self.__pdf = reader(pdf_file_path)

        # ��ȡPDF�ļ���������·����
        self.file_name = os.path.basename(pdf_file_path)
        # PDF�ļ�Ԫ����
        self.metadata = self.__pdf.getXmpMetadata()
        # �ĵ���Ϣ
        self.doc_info = self.__pdf.getDocumentInfo()
        # ҳ��
        self.pages_num = self.__pdf.getNumPages()

        # ��д��PDF���󣬸��ݲ�ͬ��ģʽ���г�ʼ��
        self.__writeable_pdf = writer()
        if mode == PDFHandleMode.COPY:
            self.__writeable_pdf.cloneDocumentFromReader(self.__pdf)
        elif mode == PDFHandleMode.NEWLY:
            for idx in range(self.pages_num):
                page = self.__pdf.getPage(idx)
                self.__writeable_pdf.insertPage(page, idx)

    def save2file(self,new_file_name):
        '''
        ���޸ĺ��PDF������ļ�
        :param new_file_name: ���ļ�������Ҫ��ԭ�ļ�����ͬ
        :return: None
        '''
        # �����޸ĺ��PDF�ļ����ݵ��ļ���
        with open(new_file_name, 'wb') as fout:
            self.__writeable_pdf.write(fout)
        print('save2file success! new file is: {0}'.format(new_file_name))

    def add_one_bookmark(self,title,page,parent = None, color = None,fit = '/Fit'):
        '''
        ��PDF�ļ�����ӵ�����ǩ�����ұ���Ϊһ���µ�PDF�ļ�
        :param str title: ��ǩ����
        :param int page: ��ǩ��ת����ҳ�룬��ʾ����PDF�еľ���ҳ�룬ֵΪ1��ʾ��һҳ
        :paran parent: A reference to a parent bookmark to create nested bookmarks.
        :param tuple color: Color of the bookmark as a red, green, blue tuple from 0.0 to 1.0
        :param list bookmarks: ��һ��'(��ǩ���⣬ҳ��)'��Ԫ���б�������[(u'tag1',1),(u'tag2',5)]��ҳ��Ϊ1�����һҳ
        :param str fit: ��ת����ǩҳ������ŷ�ʽ
        :return: None
        '''
        # Ϊ�˷�ֹ���룬�����title����utf-8����
        self.__writeable_pdf.addBookmark(title.decode('utf-8'),page - 1,parent = parent,color = color,fit = fit)
        print('add_one_bookmark success! bookmark title is: {0}'.format(title))

    def add_bookmarks(self,bookmarks):
        '''
        ���������ǩ
        :param bookmarks: ��ǩԪ���б����е�ҳ���ʾ����PDF�еľ���ҳ�룬ֵΪ1��ʾ��һҳ
        :return: None
        '''
        for title,page in bookmarks:
            self.add_one_bookmark(title,page)
        print('add_bookmarks success! add {0} pieces of bookmarks to PDF file'.format(len(bookmarks)))

    def read_bookmarks_from_txt(self,pbm_file_path,page_offset = 0):
        '''
        ���ı��ļ��ж�ȡ��ǩ�б�
        �ı��ļ��������У�ÿ��һ����ǩ�����ݸ�ʽΪ��
        ��ǩ���� ҳ��
        ע���м��ÿո������ҳ��Ϊ1��ʾ��1ҳ
        :param pbm_file_path: ��ǩ��Ϣ�ı��ļ�·��
        :param page_offset: ҳ���������Ϊ0�������������ڷ��桢Ŀ¼��ҳ��Ĵ��ڣ���PDF��ʵ�ʵľ���ҳ�����Ŀ¼��д��ҳ�����Ĳ�ֵ
        :return: ��ǩ�б�
        '''
        bookmarks = []
        with open(pbm_file_path,'r') as fin:
            for line in fin:
                line = line.rstrip()
                if not line:
                    continue
                # ��'@'��Ϊ���⡢ҳ��ָ���
                print('read line is: {0}'.format(line))
                try:
                    title = line.split('@')[0].rstrip()
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    print msg
                    continue
                # title��page����Ϊ�ղ������ǩ���������
                if title and page:
                    try:
                        page = int(page) + page_offset
                        bookmarks.append((title, page))
                    except ValueError as msg:
                        print(msg)

        return bookmarks

    def add_bookmarks_by_read_txt(self,pbm_file_path,page_offset = 0):
        '''
        ͨ����ȡ��ǩ�б���Ϣ�ı��ļ�������ǩ������ӵ�PDF�ļ���
        :param pbm_file_path: ��ǩ�б���Ϣ�ı��ļ�
        :param page_offset: ҳ���������Ϊ0�������������ڷ��桢Ŀ¼��ҳ��Ĵ��ڣ���PDF��ʵ�ʵľ���ҳ�����Ŀ¼��д��ҳ�����Ĳ�ֵ
        :return: None
        '''
        bookmarks = self.read_bookmarks_from_txt(pbm_file_path,page_offset)
        self.add_bookmarks(bookmarks)
        print('add_bookmarks_by_read_txt success!')
