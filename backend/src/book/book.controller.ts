import {
  Body,
  Controller,
  Get,
  NotFoundException,
  Param,
  Post,
} from '@nestjs/common';
import { BookService } from './book.service';
import { BookCreateDto } from './dto/book-create.dto';
import { BookFilterDto } from './dto/book-filter.dto';
import { I18nService } from 'nestjs-i18n';

@Controller('book')
export class BookController {
  constructor(
    private bookService: BookService,
    private i18n: I18nService,
  ) {}

  @Post()
  async create(@Body() dto: BookCreateDto) {
    return await this.bookService.create(dto);
  }

  @Get(':id')
  async findOneById(@Param() dto: BookFilterDto) {
    const bookInDb = await this.bookService.findOneById(dto.id);

    if (!bookInDb) {
      throw new NotFoundException(this.i18n.t('validation.NOT_FOUND'));
    }

    return bookInDb;
  }
}
