import {
  BadRequestException,
  Controller,
  Delete,
  Get,
  Param,
  Post,
} from '@nestjs/common';
import { SearchService } from './search.service';
import { ApiTags } from '@nestjs/swagger';
import { I18nService } from 'nestjs-i18n';

@ApiTags('search')
@Controller('search')
export class SearchController {
  constructor(
    private searchService: SearchService,
    private i18n: I18nService,
  ) {}

  @Post('index')
  async createIndex() {
    const indexInDb = await this.searchService.getIndex();
    if (indexInDb?.book) {
      throw new BadRequestException(this.i18n.t('validation.ALREADY_EXISTS'));
    }

    return await this.searchService.createIndex();
  }

  @Get('index')
  async getIndex() {
    return await this.searchService.getIndex();
  }

  @Delete('index')
  async deleteIndex() {
    return await this.searchService.deleteIndex();
  }

  @Get(':text')
  async search(@Param('text') text: string) {
    const result = await this.searchService.search(text);
    return result.hits.hits.map((val) => val._source);
  }
}
